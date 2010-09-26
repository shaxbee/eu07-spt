"""
Class with the ribbon menubar instance

Created on 2010-09-22

@author: gfirlejczyk
"""

import os.path
import wx

import wx.lib.agw.ribbon as RB
class RibbonPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY,size=wx.Size(30,103))

        self._ribbon = RB.RibbonBar(self, wx.ID_ANY)

        home = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Home", wx.NullBitmap)
        toolbar_panel = RB.RibbonPanel(home, wx.ID_ANY, "File tools", wx.NullBitmap, wx.DefaultPosition,
                                       wx.DefaultSize, agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        s = wx.BoxSizer(wx.VERTICAL)

        s.Add(self._ribbon, 0, wx.EXPAND)
        self.SetSizer(s)

