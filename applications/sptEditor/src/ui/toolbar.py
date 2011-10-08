'''
Created on 23-07-2011

@author: gfirlejczyk
'''
import os.path
import wx
import sys


import ui.flatmenu as FM
from wx.lib.agw.artmanager import ArtManager
#from wx.lib.agw.fmresources import ControlFocus, ControlPressed
from wx.lib.agw.fmresources import FM_OPT_SHOW_CUSTOMIZE, FM_OPT_SHOW_TOOLBAR, FM_OPT_MINIBAR, FM_OPT_IS_LCD

#this globals are overwrite by globals in application.py

ID_EXPORT = wx.ID_HIGHEST
ID_CENTER_AT = ID_EXPORT +1
ID_INSERT_TRACK = ID_CENTER_AT +1
ID_INSERT_SWITCH = ID_INSERT_TRACK +1
ID_INSERT_CURVE = ID_INSERT_SWITCH +1
ID_MODE_TRACK_NORMAL = ID_INSERT_CURVE  + 1
ID_MODE_TRACK_CLOSURE = ID_MODE_TRACK_NORMAL + 1

class ToolBarPanel(wx.Panel):
    
    def __init__(self, parent):
        #wx.Panel.__init__(self, parent, wx.ID_ANY,size=wx.Size(30,103))
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        
        dirName = os.path.dirname(os.path.abspath(sys.argv[0]))
        bitmapDir = os.path.join(dirName, 'icons')
        self.bitmap_action_dir = os.path.join(bitmapDir, 'actions')
        
        self._mb = FM.FlatMenuBar(self, wx.ID_ANY, 48, 5, options = FM_OPT_IS_LCD | FM_OPT_MINIBAR | FM_OPT_SHOW_TOOLBAR | FM_OPT_SHOW_CUSTOMIZE)
        self._mb.GetRendererManager().SetTheme(FM.Style2007)
        
        self.CreateToolBar()
        
        self.BindButtons()
        
        s = wx.BoxSizer(wx.VERTICAL)
        s.Add(self._mb, 0, wx.EXPAND)
        self.SetSizer(s)
        
        ArtManager.Get().SetMBVerticalGradient(True)
        ArtManager.Get().SetRaiseToolbar(False)
        
        self._mb.Refresh()
        
    def CreateToolBar(self):
                
        icon_open = wx.Bitmap(os.path.join(self.bitmap_action_dir, "document-open.png"), wx.BITMAP_TYPE_PNG)
        icon_new = wx.Bitmap(os.path.join(self.bitmap_action_dir, "document-new.png"), wx.BITMAP_TYPE_PNG)
        icon_save = wx.Bitmap(os.path.join(self.bitmap_action_dir, "document-save.png"), wx.BITMAP_TYPE_PNG)
        icon_saveas = wx.Bitmap(os.path.join(self.bitmap_action_dir, "media-floppy.png"), wx.BITMAP_TYPE_PNG)
        icon_export = wx.Bitmap(os.path.join(self.bitmap_action_dir, "application-x-bittorrent.png"), wx.BITMAP_TYPE_PNG)

        self._mb.AddTool(wx.ID_NEW, "New", icon_new)
        self._mb.AddTool(wx.ID_OPEN, "Open", icon_open)
        self._mb.AddTool(wx.ID_SAVE, "Save", icon_save)
        self._mb.AddTool(wx.ID_SAVEAS, "Saveas", icon_saveas)
        self._mb.AddTool(ID_EXPORT, "Export", icon_export)
        
        self._mb.AddSeparator()
        
        icon_delete = wx.Bitmap(os.path.join(self.bitmap_action_dir, "edit-delete.png"), wx.BITMAP_TYPE_PNG)
        icon_undo = wx.Bitmap(os.path.join(self.bitmap_action_dir, "edit-undo.png"), wx.BITMAP_TYPE_PNG)
        icon_redo = wx.Bitmap(os.path.join(self.bitmap_action_dir, "edit-redo.png"), wx.BITMAP_TYPE_PNG)
        
        self._mb.AddTool(wx.ID_DELETE, "Delete", icon_delete)
        self._mb.AddTool(wx.ID_UNDO, "Undo", icon_undo)
        self._mb.AddTool(wx.ID_REDO, "Redo", icon_redo)
        
        self._mb.AddSeparator()
        
        icon_centerat = wx.Bitmap(os.path.join(self.bitmap_action_dir, "view-restore.png"), wx.BITMAP_TYPE_PNG)
        icon_zoomin = wx.Bitmap(os.path.join(self.bitmap_action_dir, "zoom-in.png"), wx.BITMAP_TYPE_PNG)
        icon_zoomout = wx.Bitmap(os.path.join(self.bitmap_action_dir, "zoom-out.png"), wx.BITMAP_TYPE_PNG)

        self._mb.AddTool(ID_CENTER_AT, "Center At", icon_centerat)
        self._mb.AddTool(wx.ID_ZOOM_IN, "Zoom In", icon_zoomin)
        self._mb.AddTool(wx.ID_ZOOM_OUT, "Zoom Out", icon_zoomout)
        
        # This will'be not needed
        '''
        self._mb.AddSeparator()
        
        icon_insert_track = wx.Bitmap(os.path.join(self.bitmap_action_dir, "insert_straight.png"), wx.BITMAP_TYPE_PNG)
        icon_insert_switch = wx.Bitmap(os.path.join(self.bitmap_action_dir, "insert_switch.png"), wx.BITMAP_TYPE_PNG)
        icon_insert_curve = wx.Bitmap(os.path.join(self.bitmap_action_dir, "insert_curve.png"), wx.BITMAP_TYPE_PNG)
        
        self._mb.AddTool(ID_INSERT_TRACK, "Insert track", icon_insert_track)
        self._mb.AddTool(ID_INSERT_CURVE, "Insert curve", icon_insert_curve)
        self._mb.AddTool(ID_INSERT_SWITCH, "Insert switch", icon_insert_switch)
        '''
        self._mb.AddSeparator()
        
        icon_normal = wx.Bitmap(os.path.join(self.bitmap_action_dir, "transform-crop-and-resize.png"), wx.BITMAP_TYPE_PNG)
        icon_closure = wx.Bitmap(os.path.join(self.bitmap_action_dir, "transmission.png"), wx.BITMAP_TYPE_PNG)
        
        self._mb.AddRadioTool(ID_MODE_TRACK_NORMAL, "Mode normal", icon_normal)
        self._mb.AddRadioTool(ID_MODE_TRACK_CLOSURE, "Mode closure (flex)", icon_closure)
        
    def BindButtons(self):
        #InsertPanel
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.GetParent().OnInsertStraightTrack, id=ID_INSERT_TRACK)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.GetParent().OnInsertCurveTrack, id=ID_INSERT_CURVE)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.GetParent().OnInsertRailSwitch, id=ID_INSERT_SWITCH)
        
        #HistoryPanel
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.GetParent().OnDelete, id=wx.ID_DELETE)
        
        #FilePanel
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.GetParent().OnNew, id=wx.ID_NEW)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.GetParent().OnOpen, id=wx.ID_OPEN)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.GetParent().OnSave, id=wx.ID_SAVE)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.GetParent().OnSaveAs, id=wx.ID_SAVEAS)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.GetParent().OnExport, id=ID_EXPORT)
       
        #NavigationPanel
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.GetParent().OnCenterAt, id=ID_CENTER_AT)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.GetParent().OnZoomIn, id=wx.ID_ZOOM_IN)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.GetParent().OnZoomOut, id=wx.ID_ZOOM_OUT)
        
        #Editor mode
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.GetParent().OnChangeEditorMode, id=ID_MODE_TRACK_NORMAL)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.GetParent().OnChangeEditorMode, id=ID_MODE_TRACK_CLOSURE)
    
    def SelectButton(self, id):
        '''Select button from menu'''
        self._mb.SetSelection(id)
        
    