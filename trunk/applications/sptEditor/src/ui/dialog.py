"""
This module contains all dialogs defined in editor application.

@author adammo
"""

import math
import wx

import ui.editor


class CenterAtDialog(wx.Dialog):
    """
    Dialog box for centering view at specified scenery point.
    """
    
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Center at")
        self.SetMinSize(wx.Size(200, 200))

        panel = wx.Panel(self, wx.ID_ANY)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.CreateContent(panel)

        okButton = wx.Button(self, wx.ID_OK, "Ok", wx.DefaultPosition, \
            wx.DefaultSize)
        closeButton = wx.Button(self, wx.ID_CANCEL, "Cancel", \
            wx.DefaultPosition, wx.DefaultSize)

        self.Bind(wx.EVT_BUTTON, self.OnButton, okButton)

        hbox.Add(okButton, 1)
        hbox.Add(closeButton, 1, wx.LEFT, 5)

        vbox.Add(panel, 1)
        vbox.Add(hbox, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)

        self.SetSizer(vbox)

        self.Fit()
        self.Centre()
        self.ShowModal()

        self.Destroy()


    def CreateContent(self, panel):

        sizer = wx.FlexGridSizer(3, 2, 5, 5)
       
        self.x = wx.TextCtrl(panel, wx.ID_ANY, "%.3f" % 0, \
                             style = wx.TE_RIGHT, name = "x")
        self.y = wx.TextCtrl(panel, wx.ID_ANY, "%.3f" % 0, \
                             style = wx.TE_RIGHT, name = "y")
        self.z = wx.TextCtrl(panel, wx.ID_ANY, "%.3f" % 0, \
                             style = wx.TE_RIGHT, name = "z")
 
        sizer.Add( wx.StaticText(panel, wx.ID_ANY, "X:"), 0, wx.ALIGN_RIGHT )
        sizer.Add( self.x, 1, wx.EXPAND )
        sizer.Add( wx.StaticText(panel, wx.ID_ANY, "Y:"), 0, wx.ALIGN_RIGHT )
        sizer.Add( self.y, 1, wx.EXPAND )
        sizer.Add( wx.StaticText(panel, wx.ID_ANY, "Z:"), 0, wx.ALIGN_RIGHT )
        sizer.Add( self.z, 1, wx.EXPAND )

        panel.SetSizer(sizer)


    def OnButton(self, event):
        """
        Sets the scroll to the editor part.
        """       
        try: 
            px = float(self.x.GetValue())
            py = float(self.y.GetValue())
            pz = float(self.z.GetValue())

            editor = self.GetParent().editor
            (vx, vy) = editor.parts[0].ModelToView((px, py, pz))
            editor.parts[0].CenterViewAt(vx, vy)

            self.Destroy()
        except ValueError: 
            # Swallow number pasing error
            pass




class BasePointDialog(wx.Dialog):
    """
    Dialog for manipulating base point positions and angles.
    """
    
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Base point location")
        self.SetMinSize(wx.Size(200, 200))
        
        panel = wx.Panel(self, wx.ID_ANY)
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.CreateContent(panel)

        okButton = wx.Button(self, wx.ID_OK, "Ok", wx.DefaultPosition, \
            wx.DefaultSize)
        closeButton = wx.Button(self, wx.ID_CANCEL, "Cancel", \
            wx.DefaultPosition, wx.DefaultSize)

        self.Bind(wx.EVT_BUTTON, self.OnButton, okButton)

        hbox.Add(okButton, 1)
        hbox.Add(closeButton, 1, wx.LEFT, 5)

        vbox.Add(panel, 1)
        vbox.Add(hbox, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)

        self.SetSizer(vbox)

        self.Fit()
        self.Centre()
        self.ShowModal()

        self.Destroy()


    def CreateContent(self, panel):
        basePoint = self.GetParent().editor.basePoint
        if basePoint == None:
            basePoint = ui.editor.BasePoint((0.0, 0.0, 0.0), 0, 0)

        sizer = wx.FlexGridSizer(5, 2, 5, 5)
       
        self.x = wx.TextCtrl(panel, wx.ID_ANY, "%.3f" % basePoint.point[0], \
                             style = wx.TE_RIGHT, name = "x")
        self.y = wx.TextCtrl(panel, wx.ID_ANY, "%.3f" % basePoint.point[1], \
                             style = wx.TE_RIGHT, name = "y")
        self.z = wx.TextCtrl(panel, wx.ID_ANY, "%.3f" % basePoint.point[2], \
                             style = wx.TE_RIGHT, name = "z")
        self.alpha = wx.TextCtrl(panel, wx.ID_ANY, "%.2f" % basePoint.alpha, \
                             style = wx.TE_RIGHT, name = "alpha")
        self.beta = wx.TextCtrl(panel, wx.ID_ANY, "%.2f" % basePoint.beta, \
                             style = wx.TE_RIGHT, name = "beta")
 
        sizer.Add( wx.StaticText(panel, wx.ID_ANY, "X:"), 0, wx.ALIGN_RIGHT )
        sizer.Add( self.x, 1, wx.EXPAND )
        sizer.Add( wx.StaticText(panel, wx.ID_ANY, "Y:"), 0, wx.ALIGN_RIGHT )
        sizer.Add( self.y, 1, wx.EXPAND )
        sizer.Add( wx.StaticText(panel, wx.ID_ANY, "Z:"), 0, wx.ALIGN_RIGHT )
        sizer.Add( self.z, 1, wx.EXPAND )
        sizer.Add( wx.StaticText(panel, wx.ID_ANY, "Alpha:"), 0, \
                   wx.ALIGN_RIGHT )
        sizer.Add( self.alpha, 1, wx.EXPAND )
        sizer.Add( wx.StaticText(panel, wx.ID_ANY, "Beta:"), 0, \
                   wx.ALIGN_RIGHT )
        sizer.Add( self.beta, 1, wx.EXPAND )
        

        panel.SetSizer(sizer)


    def OnButton(self, event):
        '''
        Sets the scroll to the editor part.
        '''
        try: 
            px = float(self.x.GetValue())
            py = float(self.y.GetValue())
            pz = float(self.z.GetValue())
            alpha = float(self.alpha.GetValue())
            beta = float(self.beta.GetValue())

            editor = self.GetParent().editor
            editor.SetBasePoint(ui.editor.BasePoint((px, py, pz), alpha, beta))
            #(vx, vy) = editor.parts[0].ModelToView((px, py, pz))
            #editor.parts[0].CenterViewAt(vx, vy)

            self.Destroy()
        except ValueError: 
            # Swallow number pasing error
            pass

