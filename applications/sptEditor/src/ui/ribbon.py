"""
Class with the ribbon menubar instance

Created on 2010-09-22

@author: gfirlejczyk
"""

import os.path
import wx

import wx.lib.agw.ribbon as RB
#import images


# Some constants for ribbon buttons
ID_CIRCLE = wx.ID_HIGHEST + 1
ID_CROSS = ID_CIRCLE + 1
ID_TRIANGLE = ID_CIRCLE + 2
ID_SQUARE = ID_CIRCLE + 3
ID_POLYGON = ID_CIRCLE + 4
ID_SELECTION_EXPAND_H = ID_CIRCLE + 5
ID_SELECTION_EXPAND_V = ID_CIRCLE + 6
ID_SELECTION_CONTRACT = ID_CIRCLE + 7
ID_PRIMARY_COLOUR = ID_CIRCLE + 8
ID_SECONDARY_COLOUR = ID_CIRCLE + 9
ID_DEFAULT_PROVIDER = ID_CIRCLE + 10
ID_AUI_PROVIDER = ID_CIRCLE + 11
ID_MSW_PROVIDER = ID_CIRCLE + 12
ID_MAIN_TOOLBAR = ID_CIRCLE + 13
ID_POSITION_TOP = ID_CIRCLE + 14
ID_POSITION_TOP_ICONS = ID_CIRCLE + 15
ID_POSITION_TOP_BOTH = ID_CIRCLE + 16
ID_POSITION_LEFT = ID_CIRCLE + 17
ID_POSITION_LEFT_LABELS = ID_CIRCLE + 18
ID_POSITION_LEFT_BOTH = ID_CIRCLE + 19

def CreateRibbonBar(self):
    # initialize of ribbon
    #ribbon = RB.RibbonBar(self,wx.ID_ANY)

    # creating home page
    #home_page = RB.RibbonPage(ribbon,wx.ID_ANY,"Home")

    # creating panels for home page
    #main_panel = RB.RibbonPanel(home_page,wx.ID_ANY,"Main", \
    #agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)

    #adding icons
    #main_panel.AddSimpleButton(wx.ID_ANY,"New",wx.Nullbitmap,"")
    #main_panel.AddSimpleButton(wx.ID_ANY,"Open",wx.Nullbitmap,"")
    #main_panel.AddSimpleButton(wx.ID_ANY,"Save",wx.Nullbitmap,"")
    #main_panel.AddSimpleButton(wx.ID_ANY,"Save as...",wx.Nullbitmap,"")

    # create ribbon
    #ribbon.Realize()
    #return ribbon
    pass

class RibbonFrame(wx.Panel):

    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, log=None):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self.ribbon = RB.RibbonBar(self, wx.ID_ANY)
        # creating home page
        home_page = RB.RibbonPage(self.ribbon,wx.ID_ANY,"Home")

        # creating panels for home page
        #main_panel = RB.RibbonPanel(home_page,wx.ID_ANY,"Main", \
        #agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)

        #adding icons
        #main_panel.AddSimpleButton(wx.ID_ANY,"New",wx.Nullbitmap,"")
        #main_panel.AddSimpleButton(wx.ID_ANY,"Open",wx.Nullbitmap,"")
        #main_panel.AddSimpleButton(wx.ID_ANY,"Save",wx.Nullbitmap,"")
        #main_panel.AddSimpleButton(wx.ID_ANY,"Save as...",wx.Nullbitmap,"")

        # create ribbon
        self.ribbon.Realize()

        #self._logwindow = wx.TextCtrl(self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize,
#                                      wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_LEFT | wx.TE_BESTWRAP | wx.BORDER_NONE)

        s = wx.BoxSizer(wx.VERTICAL)

        s.Add(self.ribbon, 0, wx.EXPAND)
        #s.Add(self._logwindow, 1, wx.EXPAND)

        self.SetSizer(s)

        #self.BindEvents([selection, shapes, provider_bar])

        #self.SetIcon(images.Mondrian.Icon)
        #self.CenterOnScreen()
        #self.Show()
