'''
Created on 2009-03-01

@author: adammo
'''

import logging
import wx
import yaml

import model.tracks
import model.groups
import ui.editor

class Application(wx.App):
    '''
    Application handler class.
    '''
    
    def __init__(self):
        wx.App.__init__(self)

    
    def OnInit(self):
        self.SetVendorName("SPT-Team")
        self.SetAppName("EI07")
        
        wx.FileConfig.Get()
        
        return True


    
        
class MainWindow(wx.Frame):
    '''
    Main Window of Scenery Editor.
    '''
    
    def __init__(self, parent, id):
        '''
        Creates application window.
        '''
        wx.Frame.__init__(self, parent, id, "EI07", size=(200,100))

        #self.SetIcon(wx.IconFromXPMData("w8_7.xpm"))

        self.path = None
        self.group = None

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
        '''
        Creates application main menu.
        '''

        mainMenu = wx.MenuBar()

        # Create file menu
        fileMenu = wx.Menu()
        fileMenu.Append(wx.ID_NEW, "&New")
        fileMenu.Append(wx.ID_OPEN, "&Open")
        fileMenu.Append(wx.ID_SAVE, "&Save")
        fileMenu.Append(wx.ID_SAVEAS, "Save &as")
        fileMenu.AppendSeparator()
        fileMenu.Append(wx.ID_CLOSE, "&Quit")

        mainMenu.Append(fileMenu, "&File")

        # Create help menu
        helpMenu = wx.Menu()
        helpMenu.Append(wx.ID_ABOUT, "&About")

        mainMenu.Append(helpMenu, "&Help")

        self.SetMenuBar(mainMenu)

        wx.EVT_MENU(self, wx.ID_OPEN, self.OnOpen)
        wx.EVT_MENU(self, wx.ID_SAVE, self.OnSave)
        wx.EVT_MENU(self, wx.ID_CLOSE, self.OnExit)
        wx.EVT_MENU(self, wx.ID_ABOUT, self.OnAbout)


    def CreateStatusBar(self):

        bar = wx.StatusBar(self)
        bar.SetStatusText("Ready.")

        self.SetStatusBar(bar)


    def CreateContent(self):
        '''
        Creates main content of application.
        '''

        ui.editor.SceneryEditor(self, wx.ID_ANY)


    def OnAbout(self, event):
        '''
        Displays About box.
        '''

        info = wx.AboutDialogInfo()

        info.SetName("EI07")
        info.SetVersion("3.0.0")

        wx.AboutBox(info)


    def OnExit(self, event):
        '''
        Application exit callback.

        Saves configuration options.
        '''

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


    def OnOpen(self, event):
        '''
        Opens a scenery file
        '''
        
        openDialog = wx.FileDialog(self, "Choose scenery file", \
            "", "", "Textual format (*.*)|*.*")
        openDialog.CentreOnParent()
        openDialog.SetDirectory(self.workingDirectory)
        
        if openDialog.ShowModal() == wx.ID_OK:
            path = openDialog.GetPath()
            self.path = path

            self.group = yaml.load(file(path, "r"))

        self.workingDirectory = openDialog.GetDirectory()

    def OnSave(self, event):
        '''
        Saves scenery file.
        '''

        saveDialog = wx.FileDialog(self, "Choose scenery file", \
            self.workingDirectory, "", \
            "Textual format (*.*)|*.*", wx.FD_SAVE)
        saveDialog.CentreOnParent()
        if self.path != None:
            saveDialog.SetPath(self.path)

        if saveDialog.ShowModal() == wx.ID_OK:
            self.path = saveDialog.GetPath()

            self.group = model.groups.Group()
            track = model.tracks.Track()
            self.group.insert(track)

            text = yaml.dump(self.group)
            print text

            scenery_file = open(self.path, "w")
            print scenery_file
            scenery_file.write(yaml.dump(self.group))
            scenery_file.close()

        self.workingDirectory = saveDialog.GetDirectory()


app = Application()
frame = MainWindow(None, wx.ID_ANY)
app.MainLoop()

