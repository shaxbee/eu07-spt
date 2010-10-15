"""
Class with the ribbon menubar instance

Created on 2010-09-22

@author: gfirlejczyk
"""

import os.path
import wx
import sys

import wx.lib.agw.ribbon as RB

ID_EXPORT = wx.ID_HIGHEST
ID_CENTER_AT = ID_EXPORT +1

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
        self.AddEditPage()
        
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
        filetools_panel = RB.RibbonPanel(home, wx.ID_ANY, "File", wx.NullBitmap, wx.DefaultPosition,
                                       wx.DefaultSize, agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        file_tools = RB.RibbonButtonBar(filetools_panel, wx.ID_ANY)

        # dodajemy przyciski podstawowe
        #print os.path.join(bitmapDir, "document-open.png")
        icon_open = wx.Bitmap(os.path.join(self.bitmap_action_dir, "document-open.png"), wx.BITMAP_TYPE_PNG)
        icon_new = wx.Bitmap(os.path.join(self.bitmap_action_dir, "document-new.png"), wx.BITMAP_TYPE_PNG)
        icon_save = wx.Bitmap(os.path.join(self.bitmap_action_dir, "document-save.png"), wx.BITMAP_TYPE_PNG)
        icon_saveas = wx.Bitmap(os.path.join(self.bitmap_action_dir, "media-floppy.png"), wx.BITMAP_TYPE_PNG)
        icon_export = wx.Bitmap(os.path.join(self.bitmap_action_dir, "application-x-bittorrent.png"), wx.BITMAP_TYPE_PNG)
        #self.ResizeBitmap(icon_open,wx.Size(32,32))

        file_tools.AddSimpleButton(wx.ID_NEW, "New", icon_new, "New scenery")
        file_tools.AddSimpleButton(wx.ID_OPEN, "Open",icon_open,"Open scenery")
        file_tools.AddSimpleButton(wx.ID_SAVE, "Save", icon_save,"Save")
        file_tools.AddSimpleButton(wx.ID_SAVEAS, "Save as...", icon_saveas,"Save as...")
        file_tools.AddSimpleButton(ID_EXPORT, "Export", icon_export, "Export to binary file")

        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.GetParent().OnNew, id=wx.ID_NEW)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.GetParent().OnOpen, id=wx.ID_OPEN)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.GetParent().OnSave, id=wx.ID_SAVE)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.GetParent().OnSaveAs, id=wx.ID_SAVEAS)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.GetParent().OnExport, id=ID_EXPORT)

        #pole dla nawigacji
        navi_panel = RB.RibbonPanel(home,wx.ID_ANY,"Navigtion",wx.NullBitmap)
        navi = RB.RibbonButtonBar(navi_panel, wx.ID_ANY)

        icon_centerat = wx.Bitmap(os.path.join(self.bitmap_action_dir, "view-restore.png"), wx.BITMAP_TYPE_PNG)
        icon_zoomin = wx.Bitmap(os.path.join(self.bitmap_action_dir, "zoom-in.png"), wx.BITMAP_TYPE_PNG)
        icon_zoomout = wx.Bitmap(os.path.join(self.bitmap_action_dir, "zoom-out.png"), wx.BITMAP_TYPE_PNG)

        navi.AddSimpleButton(ID_CENTER_AT, "Center at", icon_centerat, "")
        navi.AddSimpleButton(wx.ID_ZOOM_IN, "Zoom in", icon_zoomin, "")
        navi.AddSimpleButton(wx.ID_ZOOM_OUT, "Zoom out", icon_zoomout, "")

        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.GetParent().OnCenterAt, id=ID_CENTER_AT)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.GetParent().OnZoomIn, id=wx.ID_ZOOM_IN)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.GetParent().OnZoomOut, id=wx.ID_ZOOM_OUT)

    def AddEditPage(self):
        # drugi panel
        edit = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Edit", wx.NullBitmap)

        # w panelu Home tworzymy nowe pole
        insert_panel = RB.RibbonPanel(edit, wx.ID_ANY, "Insert", wx.NullBitmap, wx.DefaultPosition,
                                       wx.DefaultSize, agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
                                       
        insert = RB.RibbonButtonBar(insert_panel, wx.ID_ANY)
        icon_insert_track = wx.Bitmap(os.path.join(self.bitmap_action_dir, "applications-drawing.png"), wx.BITMAP_TYPE_PNG)
        #icon_insert_curve = wx.Bitmap(os.path.join(self.bitmap_action_dir, "document-new.png"), wx.BITMAP_TYPE_PNG)
        #icon_save = wx.Bitmap(os.path.join(self.bitmap_action_dir, "document-save.png"), wx.BITMAP_TYPE_PNG)
        #icon_saveas = wx.Bitmap(os.path.join(self.bitmap_action_dir, "media-floppy.png"), wx.BITMAP_TYPE_PNG)
        #icon_export = wx.Bitmap(os.path.join(self.bitmap_action_dir, "application-x-bittorrent.png"), wx.BITMAP_TYPE_PNG)

        insert.AddSimpleButton(wx.ID_ANY, "Track", icon_insert_track, "")
        insert.AddSimpleButton(wx.ID_ANY, "Curve", icon_insert_track, "")
        insert.AddSimpleButton(wx.ID_ANY, "Switch", icon_insert_track, "")
                
        
        delete_panel = RB.RibbonPanel(edit, wx.ID_ANY, "Delete", wx.NullBitmap, wx.DefaultPosition,
                                       wx.DefaultSize, agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
                                       
        delete_bb = RB.RibbonButtonBar(delete_panel, wx.ID_ANY)
        
        icon_delete = wx.Bitmap(os.path.join(self.bitmap_action_dir, "edit-delete.png"), wx.BITMAP_TYPE_PNG)
        
        delete_bb.AddSimpleButton(wx.ID_ANY, "Delete", icon_delete, "")
        