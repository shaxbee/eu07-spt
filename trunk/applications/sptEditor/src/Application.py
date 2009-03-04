'''
Created on 2009-03-01

@author: adammo
'''

import logging
import wx

import Track

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

        self.CreateMenu()

        config = wx.FileConfig.Get()
	
        posX = config.ReadInt("/EIFrame/x", 14)
        posY = config.ReadInt("/EIFrame/y", 14)
        width = config.ReadInt("/EIFrame/width", 680)
        height = config.ReadInt("/EIFrame/height", 420)
        self.workingDirectory = config.Read("/EIAPP/workingDirectory", \
            wx.GetHomeDir())

        self.Move((posX, posY))
        self.SetSize((width, height))

        self.Bind(wx.EVT_CLOSE, self.OnExit)

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
        wx.EVT_MENU(self, wx.ID_CLOSE, self.OnExit)
        wx.EVT_MENU(self, wx.ID_ABOUT, self.OnAbout)        


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

        config.WriteInt("/EIFrame/x", pos.x)
        config.WriteInt("/EIFrame/y", pos.y)
        config.WriteInt("/EIFrame/width", size.width)
        config.WriteInt("/EIFrame/height", size.height)
        config.Write("/EIApp/workingDirectory", self.workingDirectory)

	self.Destroy()


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
            
            track = Track.Track()
            print track
            
            track2 = Track.Track((1,2,3),(1,0.5,2),(0,0,0),(2,3,1))
            print track2
            
            track3 = Track.Track()            
            
            print track == track2
            print track == track3

            logging.warn(path)

        self.workingDirectory = openDialog.GetDirectory()


app = Application()
frame = MainWindow(None, wx.ID_ANY)
app.MainLoop()

