"""
Class with the ribbon menubar instance

Created on 2010-09-22

@author: gfirlejczyk
"""

import os.path
import yaml
import wx

import Application
import model.tracks
import ui.dialog
import ui.trackfc
import sptyaml

import wx.lib.agw.ribbon as RB
import images


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

class RibbonFrame(wx.Frame):

    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, log=None):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self._ribbon = RB.RibbonBar(self, wx.ID_ANY)

        self._bitmap_creation_dc = wx.MemoryDC()
        self._colour_data = wx.ColourData()

        home = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Examples", CreateBitmap("ribbon"))
        toolbar_panel = RB.RibbonPanel(home, wx.ID_ANY, "Toolbar", wx.NullBitmap, wx.DefaultPosition,
                                       wx.DefaultSize, agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)

        toolbar = RB.RibbonToolBar(toolbar_panel, ID_MAIN_TOOLBAR)
        toolbar.AddTool(wx.ID_ANY, CreateBitmap("align_left"))
        toolbar.AddTool(wx.ID_ANY, CreateBitmap("align_center"))
        toolbar.AddTool(wx.ID_ANY, CreateBitmap("align_right"))
        toolbar.AddSeparator()
        toolbar.AddHybridTool(wx.ID_NEW, wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_OTHER, wx.Size(16, 15)))
        toolbar.AddTool(wx.ID_ANY, wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, wx.Size(16, 15)))
        toolbar.AddTool(wx.ID_ANY, wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_OTHER, wx.Size(16, 15)))
        toolbar.AddTool(wx.ID_ANY, wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_OTHER, wx.Size(16, 15)))
        toolbar.AddSeparator()
        toolbar.AddDropdownTool(wx.ID_UNDO, wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_OTHER, wx.Size(16, 15)))
        toolbar.AddDropdownTool(wx.ID_REDO, wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_OTHER, wx.Size(16, 15)))
        toolbar.AddSeparator()
        toolbar.AddTool(wx.ID_ANY, wx.ArtProvider.GetBitmap(wx.ART_REPORT_VIEW, wx.ART_OTHER, wx.Size(16, 15)))
        toolbar.AddTool(wx.ID_ANY, wx.ArtProvider.GetBitmap(wx.ART_LIST_VIEW, wx.ART_OTHER, wx.Size(16, 15)))
        toolbar.AddSeparator()
        toolbar.AddHybridTool(ID_POSITION_LEFT, CreateBitmap("position_left"))
        toolbar.AddHybridTool(ID_POSITION_TOP, CreateBitmap("position_top"))
        toolbar.AddSeparator()
        toolbar.AddHybridTool(wx.ID_PRINT, wx.ArtProvider.GetBitmap(wx.ART_PRINT, wx.ART_OTHER, wx.Size(16, 15)))
        toolbar.SetRows(2, 3)

        selection_panel = RB.RibbonPanel(home, wx.ID_ANY, "Selection", CreateBitmap("selection_panel"))
        selection = RB.RibbonButtonBar(selection_panel)
        selection.AddSimpleButton(ID_SELECTION_EXPAND_V, "Expand Vertically", CreateBitmap("expand_selection_v"), "")
        selection.AddSimpleButton(ID_SELECTION_EXPAND_H, "Expand Horizontally", CreateBitmap("expand_selection_h"), "")
        selection.AddSimpleButton(ID_SELECTION_CONTRACT, "Contract", CreateBitmap("auto_crop_selection"),
                                  CreateBitmap("auto_crop_selection_small"))

        shapes_panel = RB.RibbonPanel(home, wx.ID_ANY, "Shapes", CreateBitmap("circle_small"))
        shapes = RB.RibbonButtonBar(shapes_panel)
        shapes.AddSimpleButton(ID_CIRCLE, "Circle", CreateBitmap("circle"), CreateBitmap("circle_small"))
        shapes.AddSimpleButton(ID_CROSS, "Cross", CreateBitmap("cross"), "")
        shapes.AddHybridButton(ID_TRIANGLE, "Triangle", CreateBitmap("triangle"))
        shapes.AddSimpleButton(ID_SQUARE, "Square", CreateBitmap("square"), "")
        shapes.AddDropdownButton(ID_POLYGON, "Other Polygon", CreateBitmap("hexagon"), "")

        dummy_1 = RB.RibbonPanel(home, wx.ID_ANY, "Another Panel", wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
                                 agwStyle=RB.RIBBON_PANEL_EXT_BUTTON)

        label_font = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT)
        self._bitmap_creation_dc.SetFont(label_font)

        scheme = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Appearance", CreateBitmap("eye"))
        self._default_primary, self._default_secondary, self._default_tertiary = self._ribbon.GetArtProvider().GetColourScheme(1, 1, 1)

        provider_panel = RB.RibbonPanel(scheme, wx.ID_ANY, "Art", wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
                                        agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        provider_bar = RB.RibbonButtonBar(provider_panel, wx.ID_ANY)
        provider_bar.AddSimpleButton(ID_DEFAULT_PROVIDER, "Default Provider",
                                     wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, wx.Size(32, 32)), "")
        provider_bar.AddSimpleButton(ID_AUI_PROVIDER, "AUI Provider", CreateBitmap("aui_style"), "")
        provider_bar.AddSimpleButton(ID_MSW_PROVIDER, "MSW Provider", CreateBitmap("msw_style"), "")

        primary_panel = RB.RibbonPanel(scheme, wx.ID_ANY, "Primary Colour", CreateBitmap("colours"))
        self._primary_gallery = self.PopulateColoursPanel(primary_panel, self._default_primary, ID_PRIMARY_COLOUR)

        secondary_panel = RB.RibbonPanel(scheme, wx.ID_ANY, "Secondary Colour", CreateBitmap("colours"))
        self._secondary_gallery = self.PopulateColoursPanel(secondary_panel, self._default_secondary, ID_SECONDARY_COLOUR)

        dummy_2 = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Empty Page", CreateBitmap("empty"))
        dummy_3 = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Another Page", CreateBitmap("empty"))

        self._ribbon.Realize()

        self._logwindow = wx.TextCtrl(self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize,
                                      wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_LEFT | wx.TE_BESTWRAP | wx.BORDER_NONE)

        s = wx.BoxSizer(wx.VERTICAL)

        s.Add(self._ribbon, 0, wx.EXPAND)
        s.Add(self._logwindow, 1, wx.EXPAND)

        self.SetSizer(s)

        self.BindEvents([selection, shapes, provider_bar])

        self.SetIcon(images.Mondrian.Icon)
        self.CenterOnScreen()
        self.Show()
