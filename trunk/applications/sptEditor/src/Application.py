"""
The entry point of application.

Created on 2009-03-01

@author: adammo
"""

import logging
import logging.config
import wx
import wx.xrc
import yaml
import os.path
import sys
import optparse

import model.tracks
import model.groups
import model.scenery
import ui.editor
import ui.dialog
import sptyaml

# Stock items
ID_CENTER_AT = wx.ID_HIGHEST + 1
ID_BASEPOINT_EDIT = wx.ID_HIGHEST + 2


class Application(wx.App):
    """
    Application handler class.
    """
    
    def __init__(self):
        wx.App.__init__(self) 
        sptyaml.configureYaml()

    
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
        wx.Frame.__init__(self, parent, id, "EI07", size=(200,100))

        # Load resource file
        self.xRes = wx.xrc.XmlResource("Application.xrc")

        #self.SetIcon(wx.IconFromXPMData("w8_7.xpm"))

        self.modified = False
        self.path = None

        self.UpdateTitle()

        self.CreateMenu()
        self.CreateStatusBar()
        self.CreateContent()

        config = wx.FileConfig.Get()

        maximised = config.ReadInt("/EIFrame/maximised", 0)	
        posX = config.ReadInt("/EIFrame/x", 14)
        posY = config.ReadInt("/EIFrame/y", 14)
        width = config.ReadInt("/EIFrame/width", 680)
        height = config.ReadInt("/EIFrame/height", 420)
        self.workingDirectory = config.Read("/EIAPP/workingDirectory", \
            wx.GetHomeDir())

        self.Move((posX, posY))
        self.SetSize((width, height))
        self.Maximize(maximised)

        self.Bind(wx.EVT_CLOSE, self.OnExit)
        self.Bind(wx.EVT_MAXIMIZE, self.OnMaximise)

        self.Show(True)


    def CreateMenu(self):
        """
        Creates application main menu.
        """

        # from XRC file
        mainMenu = self.xRes.LoadMenuBar("MainMenu")
        self.SetMenuBar(mainMenu)

        # Events
        wx.EVT_MENU(self, wx.ID_NEW, self.OnNew)
        wx.EVT_MENU(self, wx.ID_OPEN, self.OnOpen)
        wx.EVT_MENU(self, wx.ID_SAVE, self.OnSave)
        wx.EVT_MENU(self, wx.ID_SAVEAS, self.OnSaveAs)
        wx.EVT_MENU(self, wx.ID_CLOSE, self.OnExit)
        wx.EVT_MENU(self, wx.xrc.XRCID('ID_CENTER_AT'), self.OnCenterAt)
        wx.EVT_MENU(self, wx.ID_ZOOM_IN, self.OnZoomIn)
        wx.EVT_MENU(self, wx.ID_ZOOM_OUT, self.OnZoomOut)
        wx.EVT_MENU(self, wx.xrc.XRCID('ID_BASEPOINT_EDIT'), self.OnBasePointEdit)
        wx.EVT_MENU(self, wx.ID_ABOUT, self.OnAbout)


    def CreateStatusBar(self):

        bar = wx.StatusBar(self)
        bar.SetFieldsCount(2)
        bar.SetStatusWidths([250, -1])
        bar.SetStatusText("Ready.")

        self.SetStatusBar(bar)


    def CreateContent(self):
        """
        Creates main content of application.
        """
        self.editor = ui.editor.SceneryEditor(self, wx.ID_ANY)


    def OnAbout(self, event):
        """
        Displays About box.
        """

        info = wx.AboutDialogInfo()

        info.SetName("EI07")
        info.SetVersion("3.0.0")

        wx.AboutBox(info)


    def OnExit(self, event):
        """
        Application exit callback.

        Saves configuration options.
        """
        if not self.CheckIfModified():
            return

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
                try:
                    scenery = yaml.load(file(path, "r"))
                    if not isinstance(scenery, model.scenery.Scenery):
                        raise Exception("Input file is not scenery")
                    self.editor.SetScenery(scenery)
                    self.modified = False
                    self.path = path
                    self.UpdateTitle()
                finally:
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
            try:
                scenery_file = open(path, "w")
                scenery_file.write(yaml.dump(self.editor.scenery))
                scenery_file.close()
                self.path = path
                self.modified = False
                self.UpdateTitle()
            finally:
                wx.EndBusyCursor()            

            return True
        except Exception, inst:
            logging.exception("Error while writing scenery into file:" \
                + path)
            wx.MessageBox("Error while writing scenery into file:\n" \
                + str(inst), \
                "Save file error", wx.OK | wx.ICON_ERROR, self)
            return False


    def NewScenery(self):
        """
        Creates new scenery.
        """
        self.editor.scenery = model.scenery.Scenery()
        self.modified = False
        self.path = "Unknown.txt"
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
                wx.YES_NO_CANCEL | wx.ICON_QUESTION, self)
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
                answer = wx.MessageBox("Overwrite existing file?", "Confirm", \
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
        if self.path == None:
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
        
        
    def OnBasePointEdit(self, event):
        dialog = ui.dialog.BasePointDialog(self)
        dialog.Show(True)


    def OnZoomIn(self, event):
        """
        Zooms in the scenery by increasing scale.
        """
        scale = self.editor.parts[0].GetScale()
        self.editor.parts[0].SetScale(scale * 2)        


    def OnZoomOut(self, event):
        """
        Zooms out the scenery by decreasing scale.
        """
        scale = self.editor.parts[0].GetScale()
        self.editor.parts[0].SetScale(scale / 2)



if __name__ == "__main__":
    usage = "Usage: %prog [options]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-l", "--logging", action="store", type="string", \
        dest="logging", help="Specifies configuration file for logging subsystem")
    (options, leftover) = parser.parse_args(sys.argv)
    
    if options.logging != None:
        logging.config.fileConfig(options.logging)
    
    app = Application()
    frame = MainWindow(None, wx.ID_ANY)
    app.MainLoop()

