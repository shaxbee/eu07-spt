"""
The entry point of application.

Created on 2009-03-01

@author: adammo
"""

#import logging
import logging.config
#import wx
import wx.xrc
import wx.aui as AUI
#import wx.lib.agw.ribbon as RB
import wx.lib.delayedresult as delayed
import yaml
import os.path
import sys
import optparse
#import run

import model.scenery
import ui.editor
import ui.dialog
import ui.palette
import sptyaml
#import ui.ribbon
import ui.toolbar
import osgwx

from ui.toolbar import ID_MODE_TRACK_NORMAL, ID_MODE_TRACK_CLOSURE
# Stock items
ID_CENTER_AT = wx.ID_HIGHEST          + 1
ID_BASEPOINT_EDIT = wx.ID_HIGHEST     + 2
ID_TRACK_PALETTE = wx.ID_HIGHEST      + 3
ID_EDITOR = wx.ID_HIGHEST             + 4
ID_MAIN_FRAME = wx.ID_HIGHEST         + 5
#ID_MODE_TRACK_NORMAL = wx.ID_HIGHEST  + 6
#ID_MODE_TRACK_CLOSURE = wx.ID_HIGHEST + 7
ID_PROPERTIES_PALLETE = wx.ID_HIGHEST + 8

NAME_TRACK_PALETTE = "Tools palette"
NAME_TRACTION_PALETTE = "Traction palette"
NAME_MAIN_EDITOR_TOP_VIEW = "Main Window"

class Application(wx.App):
    """
    Application handler class.
    """
    
    def __init__(self):
        '''
        Application constructor
        '''
        #Redirect is for right behavior on PyDev (don't open own console on prints and logmessages)
        wx.App.__init__(self,redirect=False) 

    
    def OnInit(self):
        wx.Image.AddHandler(wx.PNGHandler())
        
        self.SetVendorName("SPT-Team")
        self.SetAppName("EI07")
        
        wx.FileConfig.Get()
        
        return True


    
        
class MainWindow(wx.Frame):
    """
    Main Window of Scenery Editor.
    """
    
    def __init__(self, parent, id):
        """
        Creates application window.
        """
        wx.Frame.__init__(self, parent, id, "EI07", size=(300,200))
        self.SetMinSize((300, 200))

        # Load resource file
        self.xRes = wx.xrc.XmlResource(os.path.join(os.path.dirname(__file__),"Application.xrc"))

        self.SetIcons(self.PrepareApplicationIcons())

        self.modified = False
        self.path = None
        self.editor = None
        
        self.UpdateTitle()

        self.CreateMenu()
        
        # Ribbon need panel which can be managed by AUIManager
        self.main_content_panel = wx.Panel(self,wx.ID_ANY)

        # creating and setting sizer for ribbon and content
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        #main_sizer.Add(self.ribbon, 0, wx.EXPAND)
        main_sizer.Add(self._menubar, 0, wx.EXPAND)
        main_sizer.Add(self.main_content_panel,1,wx.EXPAND)
        self.SetSizer(main_sizer)
        
        # Prepare pane manager
        self._paneManager = AUI.AuiManager(self.main_content_panel)
        self._paneManager.SetFlags(AUI.AUI_MGR_ALLOW_FLOATING |
                                   AUI.AUI_MGR_HINT_FADE |
                                   AUI.AUI_MGR_NO_VENETIAN_BLINDS_FADE|
                                   AUI.AUI_MGR_RECTANGLE_HINT)
        
        self.CreateStatusBar()
        self.CreatePalette()
        self.CreateContent()

        #self.RestorePerspective()


        config = wx.FileConfig.Get()

        maximised = config.ReadInt("/EIFrame/maximised", 0)	
        posX = config.ReadInt("/EIFrame/x", 14)
        posY = config.ReadInt("/EIFrame/y", 14)
        width = config.ReadInt("/EIFrame/width", 680)
        height = config.ReadInt("/EIFrame/height", 420)
        self.workingDirectory = config.Read("/EIAPP/workingDirectory", \
            wx.GetHomeDir())
        self.exportDirectory = config.Read("/EIApp/exportDirectory")

        self.Move((posX, posY))
        self.SetSize((width, height))
        self.Maximize(maximised)

        self.Bind(wx.EVT_CLOSE, self.OnExit)
        self.Bind(wx.EVT_MAXIMIZE, self.OnMaximise)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)

        self.Layout()
        
        #center on center of model
        (x, y) = self.editor.ModelToView()
        self.editor.CenterViewAt(x, y)
        self.Show(True)

        #select normal mode button
        self.MenuChangeEditorMode(ui.editor.MODE_NORMAL)

    def OnMouseWheel(self, event):
        '''Tracks mouse wheel event trough many windows'''
        self.editor.OnMouseWheel(event)

    def PrepareApplicationIcons(self):
        appIcons = wx.IconBundle()
        appIconDir = os.path.join(os.path.dirname(__file__), \
            "icons", "apps")
        appIcons.AddIconFromFile(os.path.join(appIconDir, "ei07_large.png"), \
            wx.BITMAP_TYPE_ANY)
        appIcons.AddIconFromFile(os.path.join(appIconDir, "ei07_gnome.png"), \
            wx.BITMAP_TYPE_ANY)
        appIcons.AddIconFromFile(os.path.join(appIconDir, "ei07_medium.png"), \
            wx.BITMAP_TYPE_ANY)
        appIcons.AddIconFromFile(os.path.join(appIconDir, "ei07_small.png"), \
            wx.BITMAP_TYPE_ANY)
        appIcons.AddIconFromFile(os.path.join(appIconDir, "ei07_xsmall.png"), \
            wx.BITMAP_TYPE_ANY)
        return appIcons


    def CreateMenu(self):
        """
        Creates application main menu.
        """

        #self._menubar = ui.ribbon.RibbonPanel(self)
        self._menubar = ui.toolbar.ToolBarPanel(self)

    
    def CreateStatusBar(self):

        bar = wx.StatusBar(self)
        bar.SetFieldsCount(3)
        bar.SetStatusWidths([250, 250, -1])
        bar.SetStatusText("Ready.")

        self.SetStatusBar(bar)

    def CreatePalette(self):

        # Create palette
        self.trackPaletteFrame = ui.palette.ToolsPalette(self.main_content_panel,ID_TRACK_PALETTE)
        self.propertiesPaletteFrame = ui.palette.PropertiesPalette(self.main_content_panel,wx.ID_ANY)
#        self.previewPaletteFrame = osgwx.Preview3DFrame(self.main_content_panel,"Preview")
        
        # Adding palette pane to manager as child
        self._paneManager.AddPane(self.trackPaletteFrame,AUI.AuiPaneInfo().CloseButton(). \
                                  Dockable().PinButton().MinimizeButton().MaximizeButton(). \
                                  FloatingSize(wx.Size(300, 300)).MinSize(wx.Size(250,80)). \
                                  CaptionVisible().Caption(NAME_TRACK_PALETTE).Name(NAME_TRACK_PALETTE))
        
        self._paneManager.AddPane(self.propertiesPaletteFrame, AUI.AuiPaneInfo().Dockable().CloseButton(). \
                                  PinButton().MinimizeButton().MaximizeButton().CaptionVisible(). \
                                  FloatingSize(wx.Size(300, 300)).Caption("Properties"))

#        self._paneManager.AddPane(self.previewPaletteFrame, AUI.AuiPaneInfo().Dockable().CloseButton(). \
#                                  PinButton().MinimizeButton().MaximizeButton().CaptionVisible(). \
#                                  Caption("Properties"))

        self._paneManager.Update()
        
        # Bypass bug in wxWidgets, that initialization size is wrong
        self._paneManager.GetPane(self.trackPaletteFrame).MinSize(wx.Size(0,0))

    def CreateContent(self):
        """
        Creates main content of application.
        """

        # Creating new palette pane
        self.editor = ui.editor.SceneryEditor(self.main_content_panel, self, ID_EDITOR)
        self._paneManager.AddPane(self.editor, AUI.AuiPaneInfo(). Name(NAME_MAIN_EDITOR_TOP_VIEW). \
                                  Caption(NAME_MAIN_EDITOR_TOP_VIEW).Center().CenterPane())
        
        self._paneManager.Update()
        self.NewScenery()


    def RestorePerspective(self, name):
        pass

    def SavePerspective(self, name):
        pass

    def OpenPerspective(self, name):
        pass

    def OnPaneClose(self, event):
        dp = self._paneManager.GetPane(self.trackPaletteFrame).dock_proportion
        print "dock proportion"
        print dp

        name = event.GetPane().name

        if name == NAME_TRACK_PALETTE:
            self.trackPaletteMenuEntry.Check(False)

    def ChangePaneCaption(self, pallete, caption):
        pal = self._paneManager.GetPane(pallete)
        pal.caption = caption
        self._paneManager.Update()

    def OnAbout(self, event):
        """
        Displays About box.
        """

        info = wx.AboutDialogInfo()

        info.SetName("EI07")
        info.SetVersion("3.1.0")

        wx.AboutBox(info)


    def OnExit(self, event):
        """
        Application exit callback.

        Saves configuration options.
        """        
        if not self.CheckIfModified():
            return

        try:
            config = wx.FileConfig.Get()

            size = self.GetSize()
            pos = self.GetPosition()

            config.WriteInt("/EIFrame/maximised", self.IsMaximized())
            if not self.IsMaximized():
                config.WriteInt("/EIFrame/x", pos.x)
                config.WriteInt("/EIFrame/y", pos.y)
                config.WriteInt("/EIFrame/width", size.width)
                config.WriteInt("/EIFrame/height", size.height)
            config.Write("/EIApp/workingDirectory", self.workingDirectory)
            config.Write("/EIApp/exportDirectory", self.exportDirectory)
#            config.WriteInt("/EIFrame/framesPalette", self.trackPaletteMenuEntry.IsChecked())
        finally:
            self._paneManager.UnInit()
            self.Destroy()


    def OnMaximise(self, event):
        print event


    def OnNew(self, event):
        """
        Creates new scenery
        """
        if self.CheckIfModified():
            self.NewScenery()


    def OnOpen(self, event):
        """
        Called onOpen event.
        """
        if self.CheckIfModified():
            self.Open()


    def Open(self):
        """
        Opens a scenery file
        """
        
        openDialog = wx.FileDialog(self, "Choose scenery file", \
            "", "", "Textual format (*.*)|*.*")
        openDialog.CentreOnParent()
        openDialog.SetDirectory(self.workingDirectory)
        
        if openDialog.ShowModal() == wx.ID_OK:
            path = openDialog.GetPath()

            try:
                wx.BeginBusyCursor()
                sceneryFile = file(path, "r")
                try:                    
                    scenery = yaml.load(sceneryFile, sptyaml.SptLoader)
                    if not isinstance(scenery, model.scenery.Scenery):
                        raise Exception("Input file is not scenery")
                    self.editor.SetScenery(scenery)
                    self.modified = False
                    self.path = path
                    self.UpdateTitle()
                finally:
                    sceneryFile.close()
                    wx.EndBusyCursor()
            except yaml.YAMLError, inst:
                logging.warning("Error while parsing scenery file: ", exc_info=inst)
                mark_str = ""
                if hasattr(inst, "problem_mark"):
                    mark = inst.problem_mark
                    mark_str = "Line: %d, Column: %d" % (mark.line+1, mark.column+1)
                wx.MessageBox("Error while parsing scenery file:\n" \
                    + inst.problem + "\n" + mark_str, \
                    "Parsing error", wx.OK | wx.ICON_ERROR, self)
            except Exception, inst:
                logging.exception("Error while reading scenery file:")
                wx.MessageBox("Error while reading scenery file:\n" \
                    + str(inst), \
                    "Open file error", wx.OK | wx.ICON_ERROR, self)            

        self.workingDirectory = openDialog.GetDirectory()


    def OnSave(self, event):
        """
        Saves scenery file.
        """
        self.Save()


    def OnSaveAs(self, event):
        """
        Saves scenery as another file.
        """
        if self.CheckIfModified():
            self.SaveAs()


    def SaveScenery(self, path):
        """
        Saves physically scenery into file.
        """
        try:
            wx.BeginBusyCursor()
            scenery_file = open(path, "w")            
            try:
                scenery_file.write(yaml.dump(self.editor.scenery))
                self.path = path
                self.modified = False
                self.UpdateTitle()
            finally:
                scenery_file.close()              
                wx.EndBusyCursor()            

            return True
        except Exception, inst:
            logging.exception("Error while writing scenery into file:" \
                + path)
            wx.MessageBox("Error while writing scenery into file:\n" \
                + str(inst), \
                "Save file error", wx.OK | wx.ICON_ERROR, self)
            return False


    def OnExport(self, event):
        """
        Exports scenery to binary format
        """
        dialog = ui.dialog.ExportDialog(self)
        dialog.Show(True)


    def NewScenery(self):
        """
        Creates new scenery.
        """
        self.editor.SetScenery(model.scenery.Scenery())
        self.modified = False
        self.path = ""
        self.UpdateTitle()


    def CheckIfModified(self):
        """
        A method that checks if current scenery file
        is modified and should be saved?

        Returns true if the action may be called.      
        """
        if self.modified:
            answer = wx.MessageBox("There are unsaved changes in " \
                + "scenery.\nDo you want to save them?", "Save the file", \
                wx.YES_DEFAULT|wx.CANCEL|wx.ICON_QUESTION, self)
            if answer == wx.NO:
                return True
            elif answer == wx.CANCEL:
                return False
            else:
                if self.Save():
                    return True
                else:
                    return False
        else:
            return True


    def SaveAs(self):
        """
        Method that saves the scenery as.

        Returns true if the save was successful
        """

        saveDialog = wx.FileDialog(self, "Choose scenery file", \
            self.workingDirectory, "", \
            "Textual format (*.*)|*.*", wx.FD_SAVE)
        saveDialog.CentreOnParent()
        if self.path != None:
            saveDialog.SetPath(self.path)

        if saveDialog.ShowModal() == wx.ID_OK:
            path = saveDialog.GetPath()

            if os.path.exists(path):
                answer = wx.MessageBox("Overwrite existing file?", "Confirm",
                    wx.YES_NO | wx.ICON_QUESTION, self)
                if answer == wx.NO:
                    return False


            self.workingDirectory = saveDialog.GetDirectory()

            return self.SaveScenery(path)
        else:
            return False


    def Save(self):
        """
        Saves the file.
        Returns True if save was successful.
        """
        if self.path == "":
            return self.SaveAs()
        else:
            return self.SaveScenery(self.path)


    def UpdateTitle(self):
        """
        Updates frame title.
        """
        
        title = "["
        if self.path == None:
            title += "Unknown.txt"
        else:
            title += self.path
        if self.modified:
            title += " *] - "
        else:
            title += "] - "
        title += "EI07"

        self.SetTitle(title)


    def OnCenterAt(self, event):
        """
        Displays "Center At" dialog
        """
        dialog = ui.dialog.CenterAtDialog(self)
        dialog.Show(True)
        

    def OnDelete(self, event):
        selection = self.editor.GetSelection()
        if selection != None:
            scenery = self.editor.GetScenery()
            scenery.RemoveRailTracking(selection)


    def OnChangeEditorMode(self, event):
        """
        Menu event handler for changing mode of editor.
        """
        wid = event.GetId()
        if wid == ID_MODE_TRACK_NORMAL:
            self.editor.SetMode(ui.editor.MODE_NORMAL,True)
        elif wid == ID_MODE_TRACK_CLOSURE:
            self.editor.SetMode(ui.editor.MODE_CLOSURE,True)


    def OnZoomIn(self, event):
        """
        Zooms in the scenery by increasing scale.
        """
        scale = self.editor.parts[0].GetScale()
        scale.increase()
        self.editor.parts[0].SetScale(scale)


    def OnZoomOut(self, event):
        """
        Zooms out the scenery by decreasing scale.
        """
        scale = self.editor.parts[0].GetScale()
        scale.decrease()
        self.editor.parts[0].SetScale(scale)


    def OnToggleFramePalette(self, event):
        """
        Change the state of palettes
        """
        eid = event.GetId()
        if eid ==  wx.xrc.XRCID('ID_TRACK_PALETTE'):
            if event.IsChecked():
                self.OpenTrackPaletteFrame()
            else:
                self.CloseTrackPaletteFrame()


    def OpenTrackPaletteFrame(self):
        self._paneManager.RestorePane(self._trackPalettePaneInfo)
        self.trackPaletteMenuEntry.Check(True)
        self._paneManager.Update()

        #config = wx.FileConfig.Get()
        #prop = config.Read("/EIFrame/perspectiveProperties")
        #self._paneManager.LoadPerspective(prop)


    def CloseTrackPaletteFrame(self):
        '''Close palette with track models'''
        #config = wx.FileConfig.Get()
        
        #prop = self._paneManager.SavePerspective()
        #config.Write("/EIFrame/perspectiveProperties",prop)

        pi = self._paneManager.GetPane(self.trackPaletteFrame)
        pi.Hide()
        #self._paneManager.ClosePane(self._trackPalettePaneInfo)
        self._paneManager.Update()
        self.trackPaletteMenuEntry.Check(False)

    def MenuChangeEditorMode(self, mode):
        '''Change editor mode: check aprioprate button'''
        if mode == ui.editor.MODE_NORMAL:
            self._menubar.SelectButton(ID_MODE_TRACK_NORMAL)
            #self._menubar.DeselectButton(ID_MODE_TRACK_CLOSURE)
        elif mode == ui.editor.MODE_CLOSURE:
            #self._menubar.DeselectButton(ID_MODE_TRACK_NORMAL)
            self._menubar.SelectButton(ID_MODE_TRACK_CLOSURE)

if __name__ == "__main__":
    usage = "Usage: %prog [options]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-l", "--logging", action="store", type="string", \
        dest="logging", help="Specifies configuration file for logging subsystem")
    (options, leftover) = parser.parse_args(sys.argv)
    
    if options.logging != None:
        logging.config.fileConfig(options.logging)
        
    app = Application()
    frame = MainWindow(None, ID_MAIN_FRAME)
    
    #preview = osgwx.Preview3DFrame(frame, "Preview")
    
    app.MainLoop()

