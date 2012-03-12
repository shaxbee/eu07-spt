import wx
import controls

class GuiTest(wx.App):
    
    def __init__(self):
        wx.App.__init__(self, redirect = False)
        
    def OnInit(self):
        self.__frame = wx.Frame(None, -1, "Test", size=(800, 500), style=wx.DEFAULT_FRAME_STYLE)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.createPanels())
        self.__frame.SetSizer(sizer)
        
        self.__frame.CreateStatusBar(1)
        
        self.__frame.Center()
        self.__frame.Show()
        
        return True
    
    def OnClose(self):
        self.Destroy()
        
    def createPanels(self):
        panel = wx.Panel(self.__frame, -1)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)        
        self.__workspace = wx.Panel(panel, -1)
#        self.__workspace.SetSizeHints(600, 500)
        
        sizer.Add(self.__workspace, flag = wx.ALIGN_LEFT)
        
        self.__sidebar = wx.Panel(panel, -1)
#        self.__sidebar.SetSizeHints(200, 500)
        self.__sidebar.SetSizer(wx.BoxSizer(wx.VERTICAL))
        self.__sidebar.GetSizer().Add(self.createProperties())
        
        button = wx.Button(self.__sidebar, -1)
        button.Bind(wx.EVT_BUTTON, self.toggleProperties)
        self.__sidebar.GetSizer().Add(button)

        sizer.Add(self.__sidebar, flag = wx.ALIGN_RIGHT)
        
        panel.SetSizer(sizer)
        self.__panels = panel
        
        return self.__panels
    
    def createProperties(self):
        panel = wx.Panel(self.__sidebar, -1)
        input = controls.TextInput("test", "aqq")
        input.render(self.__sidebar)
        spin = controls.IntegerInput("test2", 666)
        spin.render(self.__sidebar)
        
        self.__input = input
        
        return panel
    
    def toggleProperties(self, event):
        input = self.__input
        input.visible = not input.visible
