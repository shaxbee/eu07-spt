"""
Class with the ribbon menubar instance

Created on 2010-09-22

@author: gfirlejczyk
"""

import os.path
import wx
import sys

import wx.lib.agw.ribbon as RB

class RibbonPanel(wx.Panel):
    def __init__(self, parent):
        #wx.Panel.__init__(self, parent, wx.ID_ANY,size=wx.Size(30,103))
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self._ribbon = RB.RibbonBar(self, wx.ID_ANY)

        dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

        bitmapDir = os.path.join(dirName, 'icons')
        self.bitmap_action_dir = os.path.join(bitmapDir, 'actions')
        #to tylko na pewien czas
        #bitmapDir = os.path.join(bitmapDir, 'icons')
        #sys.path.append(os.path.split(dirName)[0])

        self.AddHomePage()

        self._ribbon.Realize()
        s = wx.BoxSizer(wx.VERTICAL)

        s.Add(self._ribbon, 0, wx.EXPAND)
        self.SetSizer(s)

    def ResizeBitmap(self, bitmap, size):
        '''Method for resizing icons on bar'''
        
        img = bitmap.ConvertToImage()
        img.Rescale(size.GetWidth(), size.GetHeight(), wx.IMAGE_QUALITY_HIGH)
        return wx.BitmapFromImage(img)

    def AddHomePage(self):

        home = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Home", wx.NullBitmap)

        # w panelu Home tworzymy nowe pole
        toolbar_panel = RB.RibbonPanel(home, wx.ID_ANY, "File tools", wx.NullBitmap, wx.DefaultPosition,
                                       wx.DefaultSize, agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        toolbar = RB.RibbonButtonBar(toolbar_panel, wx.ID_ANY)

        # dodajemy przyciski podstawowe
        #print os.path.join(bitmapDir, "document-open.png")
        icon_open_doc = wx.Bitmap(os.path.join(self.bitmap_action_dir, "document-open.png"), wx.BITMAP_TYPE_PNG)
        #icon_open_doc = self.ResizeBitmap(icon_open_doc,wx.Size(32,32))

        toolbar.AddSimpleButton(wx.ID_OPEN, "Open",icon_open_doc,"Open scenery")
        toolbar.AddSimpleButton(wx.ID_SAVE, "Save", wx.Bitmap(os.path.join(self.bitmap_action_dir, "document-save.png"), wx.BITMAP_TYPE_PNG),"Save")
        toolbar.AddSimpleButton(wx.ID_SAVEAS, "Save as...",wx.Bitmap(os.path.join(self.bitmap_action_dir, "media-floppy.png"), wx.BITMAP_TYPE_PNG),"Save as...")

        #selection_panel = RB.RibbonPanel(home, wx.ID_ANY, "Selection",wx.NullBitmap)
        #selection = RB.RibbonButtonBar(selection_panel)
        #selection.AddSimpleButton(wx.ID_ANY, "Expand Vertically", wx.Bitmap(os.path.join(bitmapDir, "document-open.png")), "")
        #selection.AddSimpleButton(ID_SELECTION_EXPAND_H, "Expand Horizontally", CreateBitmap("expand_selection_h"), "")
        #selection.AddSimpleButton(ID_SELECTION_CONTRACT, "Contract", CreateBitmap("auto_crop_selection"),
        #                          CreateBitmap("auto_crop_selection_small"))

        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.GetParent().OnOpen, id=wx.ID_OPEN)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.GetParent().OnSave, id=wx.ID_SAVE)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.GetParent().OnSaveAs, id=wx.ID_SAVEAS)
