"""
Module containing palettes
"""

import os.path
import sys
import yaml
import wx
import wx.combo

import Application
import model.tracks
import ui.dialog
import ui.trackfc
import sptyaml
import math

import ui.flatmenu as FM
from wx.lib.agw.artmanager import ArtManager
#from wx.lib.agw.fmresources import ControlFocus, ControlPressed
from wx.lib.agw.fmresources import FM_OPT_SHOW_TOOLBAR, FM_OPT_MINIBAR, FM_OPT_IS_LCD

from ui.uitools import ResizeBitmap #, FindItemById, SelectButton, DeselectButton 
from sptmath import Vec3, dotProduct

#from ui.toolbar import ID_INSERT_TRACK, ID_INSERT_CURVE, ID_INSERT_SWITCH

#from Application import ID_TRACK_TOOL, ID_SWITCH_TOOL
ID_TRACK_TOOL = 1
ID_SWITCH_TOOL = 2
ID_TRACK_PROPERTIES_GRADIENT = 0
ID_TRACK_PROPERTIES_STRAIGHT = 1
ID_TRACK_PROPERTIES_ARC = 2
ID_BASEPOINT_PROPERTIES = 3

class PropertiesBaseClass:
    def OnBaseParametersChange(self):
        pass

    def SetBaseParametersStoreClass(self, store):
        pass


class ToolsPalette(wx.Panel, PropertiesBaseClass):
    def __init__(self, parent, id=wx.ID_ANY):
        wx.Panel.__init__(self,parent,id)
    
        self._tool_panel = None
        
        #create link to bitmap directory 
        dirName = os.path.dirname(os.path.abspath(sys.argv[0]))
        bitmapDir = os.path.join(dirName, 'icons')
        self.bitmap_action_dir = os.path.join(bitmapDir, 'actions')
        
        self.CreateMenu()
        
        ArtManager.Get().SetMBVerticalGradient(True)
        ArtManager.Get().SetRaiseToolbar(False)
        
        s = wx.BoxSizer(wx.VERTICAL)
        s.Add(self._menu, 0, wx.EXPAND)
        self.SetSizer(s)
      
        self._menu.Refresh()
        
        #in this dictionary insert name of class that will be load to \
        #tool panel at event from button of given ID
        self._panels = {
                        ID_TRACK_TOOL: TrackTool,
                        }
        
    def CreateMenu(self):
        '''Create menu in window'''
        self._menu = FM.FlatMenuBar(self, wx.ID_ANY, 16, 5, options = FM_OPT_IS_LCD | FM_OPT_MINIBAR | FM_OPT_SHOW_TOOLBAR)
        self._menu.GetRendererManager().SetTheme(FM.Style2007)

        #Create icons, resize it to 16 px
        icon_insert_track = ResizeBitmap(wx.Bitmap(os.path.join(self.bitmap_action_dir, "insert_straight.png"), wx.BITMAP_TYPE_PNG),16)
        icon_insert_switch = ResizeBitmap(wx.Bitmap(os.path.join(self.bitmap_action_dir, "insert_switch.png"), wx.BITMAP_TYPE_PNG),16)
        
        #adding tools
        self._menu.AddRadioTool(ID_TRACK_TOOL, "Insert track", icon_insert_track)
        self._menu.AddRadioTool(ID_SWITCH_TOOL, "Insert switch", icon_insert_switch)
       
        #binding events
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.ToolSelected, id=ID_TRACK_TOOL)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.ToolSelected, id=ID_SWITCH_TOOL)

    def ToolSelected(self, event):
        """
        Function that is called within tool selected radio buttons in menu.
        It bind id of button with appriopriate Tools panel to load.
        Bind is stored in _panels variable
        """
        if self._tool_panel != None:
            self.UnloadToolPanel()
        
        try:
            self.LoadToolPanel(self._panels[event.Id](self))
        except KeyError:
            pass
    
    def LoadToolPanel(self, panel):
        """
        Loaded tool panel under the menu.
        """
        
        self._tool_panel = self.GetSizer().Add(panel,1,wx.EXPAND).GetWindow()
        
        #Refresh
        self.Layout()
        
    def UnloadToolPanel(self):
        """
        Remove tools panel from sizer and then destroy him
        """
        
        if self.GetSizer().Remove(self._tool_panel):
            self._tool_panel.Destroy()
            self._tool_panel = None
            
            #Refresh
            self.Layout()

    def OnBaseParametersChange(self):
        pass

    def SetBaseParametersStoreClass(self, store):
        self.param_store = store 


class TrackTool(wx.Panel, PropertiesBaseClass):
    def __init__(self, parent, id = wx.ID_ANY):
        wx.Panel.__init__(self, parent, id)

        s = wx.BoxSizer(wx.VERTICAL)
        
        #Radio bos with direction selection
        self._rb = wx.RadioBox(self,wx.ID_ANY,"Direction",style=wx.RA_SPECIFY_COLS,majorDimension=3, \
                          choices=["Left","Straight","Right"], size=wx.Size(-1,50) \
                          )
        
        s.Add(self._rb,0,wx.SHAPED, wx.ALIGN_CENTER)
        
        self.SetSizer(s)
        
        #Default we set straight track
        self._rb.SetSelection(1)
        
        #Adding button for apply and cancel
        self._bOK = wx.Button(self, wx.ID_ANY, "Add")
        self.Bind(wx.EVT_BUTTON, self.AddElement)
        sb = wx.StdDialogButtonSizer()
        
        sb.AddButton(self._bOK)
        
        sb.SetAffirmativeButton(self._bOK)
        sb.Realize()
        s.AddSpacer(8)
        s.Add(sb,0,wx.EXPAND, wx.ALIGN_CENTER)
        
    def AddElement(self, event):
        """
        Adding new element
        """
        tf = ui.trackfc.TrackFactory()
        editor = self.TopLevelParent.editor 
               
        if self._rb.GetSelection() == 1 :
            track = tf.CreateStraight(100.0, editor.basePoint)
        elif self._rb.GetSelection() == 0 :
            track = tf.CreateArc(math.radians(15.0), 300, True, editor.basePoint)
        else:
            track = tf.CreateArc(math.radians(15.0), 300, False, editor.basePoint)
        
        #adding newly created track to scenery
        editor.scenery.AddRailTracking(track)
            
        #setting up new position of basepoint
        editor.SetBasePoint(editor.basePoint)
        editor.SetSelection(track)

    def OnBaseParametersChange(self):
        pass

    def SetBaseParametersStoreClass(self, store):
        self.param_store = store 


class TreeCtrlComboPopup(wx.combo.ComboPopup):
    """
    This class is a popup containing a TreeCtrl.  This time we'll 
    use a has-a style (instead of is-a like above.)
    """
    # overridden ComboPopup methods
    
    def Init(self):
        self.value = None
        self.curitem = None

        
    def Create(self, parent):
        self.tree = wx.TreeCtrl(parent, style=wx.TR_HIDE_ROOT
                                |wx.TR_HAS_BUTTONS
                                |wx.TR_SINGLE
                                |wx.TR_LINES_AT_ROOT
                                |wx.SIMPLE_BORDER)
        self.tree.Bind(wx.EVT_MOTION, self.OnMotion)
        self.tree.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        

    def GetControl(self):
        return self.tree


    def GetStringValue(self):
        if self.value:
            return self.tree.GetItemText(self.value)
        return ""


    def OnPopup(self):
        if self.value:
            self.tree.EnsureVisible(self.value)
            self.tree.SelectItem(self.value)


    def SetStringValue(self, value):
        # this assumes that item strings are unique...
        root = self.tree.GetRootItem()
        if not root:
            return
        found = self.FindItem(root, value)
        if found:
            self.value = found
            self.tree.SelectItem(found)


    def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        return wx.Size(minWidth, min(200, maxHeight))
                       

    # helpers
    
    def FindItem(self, parentItem, text):        
        item, cookie = self.tree.GetFirstChild(parentItem)
        while item:
            if self.tree.GetItemText(item) == text:
                return item
            if self.tree.ItemHasChildren(item):
                item = self.FindItem(item, text)
            item, cookie = self.tree.GetNextChild(parentItem, cookie)
        return wx.TreeItemId();


    def AddItem(self, value, parent=None):
        if not parent:
            root = self.tree.GetRootItem()
            if not root:
                root = self.tree.AddRoot("<hidden root>")
            parent = root

        item = self.tree.AppendItem(parent, value)
        return item

    
    def OnMotion(self, evt):
        # have the selection follow the mouse, like in a real combobox
        item, flags = self.tree.HitTest(evt.GetPosition())
        if item and flags & wx.TREE_HITTEST_ONITEMLABEL:
            self.tree.SelectItem(item)
            self.curitem = item
        evt.Skip()


    def OnLeftDown(self, evt):
        # do the combobox selection
        item, flags = self.tree.HitTest(evt.GetPosition())
        if item and flags & wx.TREE_HITTEST_ONITEMLABEL:
            self.curitem = item
            self.value = item
            self.Dismiss()
        evt.Skip()
        
        
class ListCtrlComboPopup(wx.ListCtrl, wx.combo.ComboPopup):
        
    def __init__(self):
        # Since we are using multiple inheritance, and don't know yet
        # which window is to be the parent, we'll do 2-phase create of
        # the ListCtrl instead, and call its Create method later in
        # our Create method.  (See Create below.)
        self.PostCreate(wx.PreListCtrl())

        # Also init the ComboPopup base class.
        wx.combo.ComboPopup.__init__(self)
        

    def AddItem(self, txt):
        self.InsertStringItem(self.GetItemCount(), txt)

    def OnMotion(self, evt):
        item, flags = self.HitTest(evt.GetPosition())
        if item >= 0:
            self.Select(item)
            self.curitem = item

    def OnLeftDown(self, evt):
        self.value = self.curitem
        self.Dismiss()


    # The following methods are those that are overridable from the
    # ComboPopup base class.  Most of them are not required, but all
    # are shown here for demonstration purposes.


    # This is called immediately after construction finishes.  You can
    # use self.GetCombo if needed to get to the ComboCtrl instance.
    def Init(self):
        self.value = -1
        self.curitem = -1


    # Create the popup child control.  Return true for success.
    def Create(self, parent):
        wx.ListCtrl.Create(self, parent,
                           style=wx.LC_LIST|wx.LC_SINGLE_SEL|wx.SIMPLE_BORDER)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        return True


    # Return the widget that is to be used for the popup
    def GetControl(self):
        #self.log.write("ListCtrlComboPopup.GetControl")
        return self

    # Called just prior to displaying the popup, you can use it to
    # 'select' the current item.
    def SetStringValue(self, val):
        idx = self.FindItem(-1, val)
        if idx != wx.NOT_FOUND:
            self.Select(idx)

    # Return a string representation of the current item.
    def GetStringValue(self):
        if self.value >= 0:
            return self.GetItemText(self.value)
        return ""

    # Called immediately after the popup is shown
    def OnPopup(self):
        wx.combo.ComboPopup.OnPopup(self)

    # Called when popup is dismissed
    def OnDismiss(self):
        wx.combo.ComboPopup.OnDismiss(self)

    # This is called to custom paint in the combo control itself
    # (ie. not the popup).  Default implementation draws value as
    # string.
    def PaintComboControl(self, dc, rect):
        wx.combo.ComboPopup.PaintComboControl(self, dc, rect)

    # Receives key events from the parent ComboCtrl.  Events not
    # handled should be skipped, as usual.
    def OnComboKeyEvent(self, event):
        wx.combo.ComboPopup.OnComboKeyEvent(self, event)

    # Implement if you need to support special action when user
    # double-clicks on the parent wxComboCtrl.
    def OnComboDoubleClick(self):
        wx.combo.ComboPopup.OnComboDoubleClick(self)

    # Return final size of popup. Called on every popup, just prior to OnPopup.
    # minWidth = preferred minimum width for window
    # prefHeight = preferred height. Only applies if > 0,
    # maxHeight = max height for window, as limited by screen size
    #   and should only be rounded down, if necessary.
    def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        return wx.combo.ComboPopup.GetAdjustedSize(self, minWidth, prefHeight, maxHeight)

    # Return true if you want delay the call to Create until the popup
    # is shown for the first time. It is more efficient, but note that
    # it is often more convenient to have the control created
    # immediately.    
    # Default returns false.
    def LazyCreate(self):
        return wx.combo.ComboPopup.LazyCreate(self)




class BaseParametersForLineandStationPalette(wx.ScrolledWindow):
    """
    Class with properties for lines and station tracks
    """
    def __init__(self, parent, id = wx.ID_ANY, w=200, h=400):
        wx.ScrolledWindow.__init__(self, parent, id)
        
        s = wx.BoxSizer(wx.VERTICAL)
        
        self.__PARAMS_LINE_PL = "Poland"
        self.__PARAMS_LINE_MAIN = "Main line"
        self.__PARAMS_LINE_FIRST_LEVEL = "First level line"
        self.__PARAMS_LINE_SEC_LEVEL = "Second level line"
        self.__PARAMS_LINE_LOCAL = "Local line"
        self.__PARAMS_STATION_MAIN = "Main track"
        self.__PARAMS_STATION_MAIN_ADD = "Main add track"
        self.__PARAMS_STATION_OTHER = "Other track"
        self.__PARAMS_TERRAIN_FLAT = "Flat terrain"
        self.__PARAMS_TERRAIN_MIDDLE = "Middle flat terrain"
        self.__PARAMS_TERRAIN_HIGHLANDS = "Highlands terrain"
        
        self.MakeUI(s)
        self.CreateContent()
        self.BindEvents()
        self.SetSizer(s)
        self.Layout()

        self.palletes = []
        

    def MakeUI(self, s):
        """
        Function in which we make some GUI for changing 
        properties of straight track
        """
        
        '''
        Angle degrees
        '''
        
#        fgs = wx.FlexGridSizer(cols=3, hgap=10, vgap=10)
        fgs = wx.FlexGridSizer(1,2,5,5)

        self.cc_line = wx.combo.ComboCtrl(self, style=wx.CB_READONLY, size=(150,-1))

        fgs.Add(wx.StaticText(self,wx.ID_ANY,"Line"),0, wx.EXPAND | wx.LEFT)
        fgs.Add(self.cc_line,1, wx.EXPAND | wx.ALIGN_CENTER)

        self.cc_station = wx.combo.ComboCtrl(self, style=wx.CB_READONLY, size=(150,-1))
        
        fgs.Add(wx.StaticText(self,wx.ID_ANY,"Station"),0, wx.EXPAND | wx.LEFT)
        fgs.Add(self.cc_station,1, wx.EXPAND | wx.ALIGN_CENTER)

#        self.cc_bocznica = wx.combo.ComboCtrl(self, style=wx.CB_READONLY, size=(150,-1))
#        
#        fgs.Add(wx.StaticText(self,wx.ID_ANY,"Bocznica"),0, wx.EXPAND | wx.LEFT)
#        fgs.Add(self.cc_bocznica,1, wx.EXPAND | wx.ALIGN_CENTER)

        self.cc_terrain = wx.combo.ComboCtrl(self, style=wx.CB_READONLY, size=(150,-1))
        
        fgs.Add(wx.StaticText(self,wx.ID_ANY,"Terrain"),0, wx.EXPAND | wx.LEFT)
        fgs.Add(self.cc_terrain,1, wx.EXPAND | wx.ALIGN_CENTER)

        self.sl_V = wx.Slider(self,wx.ID_ANY,120,0,250, size=(150,-1), \
                              style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        self.sl_V.SetTickFreq(10)
        
        fgs.Add(wx.StaticText(self,wx.ID_ANY,"Velocity"),0, wx.EXPAND | wx.LEFT)
        fgs.Add(self.sl_V,1, wx.EXPAND | wx.ALIGN_CENTER)


        s.AddSpacer(5)
        s.Add(fgs,0,wx.EXPAND)

        self._bOK = wx.Button(self, wx.ID_ANY, "Apply")

        sb = wx.StdDialogButtonSizer()
        sb.AddButton(self._bOK)
        sb.SetAffirmativeButton(self._bOK)
        sb.Realize()

        s.AddSpacer(8)
        s.Add(sb,0,wx.EXPAND)

    def CreateContent(self):
        # Add some items to the line listctrl.
        tcp = TreeCtrlComboPopup()
        self.cc_line.SetPopupControl(tcp)
#        tcp = self.cc_line.GetPopupControl()
        item = tcp.AddItem(self.__PARAMS_LINE_PL)
        
        tcp.AddItem(self.__PARAMS_LINE_MAIN, item)
        tcp.AddItem(self.__PARAMS_LINE_FIRST_LEVEL, item)
        tcp.AddItem(self.__PARAMS_LINE_SEC_LEVEL, item)
        tcp.AddItem(self.__PARAMS_LINE_LOCAL, item)
        
        tcp_st = TreeCtrlComboPopup()
        self.cc_station.SetPopupControl(tcp_st)
        
        item = tcp_st.AddItem(self.__PARAMS_LINE_PL)
        tcp_st.AddItem(self.__PARAMS_STATION_MAIN, item)
        tcp_st.AddItem(self.__PARAMS_STATION_MAIN_ADD, item)
        tcp_st.AddItem(self.__PARAMS_STATION_OTHER, item)
        
        lcp = ListCtrlComboPopup()
        self.cc_terrain.SetPopupControl(lcp)
        
        lcp.AddItem(self.__PARAMS_TERRAIN_FLAT)
        lcp.AddItem(self.__PARAMS_TERRAIN_MIDDLE)
        lcp.AddItem(self.__PARAMS_TERRAIN_HIGHLANDS)

    def BindEvents(self):
        """
        Function to bind events with combos
        """
        self.Bind(wx.EVT_BUTTON, self.OnParametersChange)        

    def OnParametersChange(self, evt):
        """
        Function to which we change parameters based on what is 
        selected by user
        """
        
        # Set max speed
        self.maxVel = self.sl_V.GetValue()
        
        # Set min and max radius for line
        l = self.cc_line.GetValue()
        t = self.cc_terrain.GetValue()
        
        if l==self.__PARAMS_LINE_PL or l==self.__PARAMS_LINE_MAIN:
            self.maxR = 15000.0
            if t==self.__PARAMS_TERRAIN_FLAT:
                self.minR = 1500.0
            elif t==self.__PARAMS_TERRAIN_MIDDLE:
                self.minR = 1200.0
            elif t==self.__PARAMS_TERRAIN_HIGHLANDS:
                self.minR = 600.0
        elif l==self.__PARAMS_LINE_FIRST_LEVEL:
            self.maxR = 15000.0
            if t==self.__PARAMS_TERRAIN_FLAT:
                self.minR = 1200.0
            elif t==self.__PARAMS_TERRAIN_MIDDLE:
                self.minR = 600.0
            elif t==self.__PARAMS_TERRAIN_HIGHLANDS:
                self.minR = 400.0
        elif l==self.__PARAMS_LINE_SEC_LEVEL:
            self.maxR = 15000.0
            if t==self.__PARAMS_TERRAIN_FLAT:
                self.minR = 600.0
            elif t==self.__PARAMS_TERRAIN_MIDDLE:
                self.minR = 400.0
            elif t==self.__PARAMS_TERRAIN_HIGHLANDS:
                self.minR = 300.0
        elif l==self.__PARAMS_LINE_LOCAL:
            self.maxR = 15000.0
            if t==self.__PARAMS_TERRAIN_FLAT:
                self.minR = 400.0
            elif t==self.__PARAMS_TERRAIN_MIDDLE:
                self.minR = 250.0
            elif t==self.__PARAMS_TERRAIN_HIGHLANDS:
                self.minR = 200.0
        
        for p in self.palletes:
            p.OnBaseParametersChange()
    
    def RegisterPalletesForChangingParametersIn(self, palette):
        """
        Function in which we registers classes to which we send
        information that base parameters was changed
        """
        
        self.palletes.append(palette)
        palette.SetBaseParametersStoreClass(self)
        

class PropertiesPalette(wx.ScrolledWindow, PropertiesBaseClass):
    """
    Base class for all properties palettes for tools
    """
    def __init__(self, parent, editor=None, id = wx.ID_ANY, w=200, h=400):
        wx.ScrolledWindow.__init__(self, parent, id)
        self.SetSizer(wx.BoxSizer(wx.VERTICAL))

        self._panels = {
                        ID_TRACK_PROPERTIES_STRAIGHT: TrackPropertiesStraight(self, editor=editor),
                        ID_BASEPOINT_PROPERTIES: BasePointProperties(self, editor=editor),
                        ID_TRACK_PROPERTIES_ARC: TrackPropertiesArc(self, editor=editor),
                        }    

        self.LoadToolProperties(self._panels[ID_TRACK_PROPERTIES_ARC])
        self.UnloadToolProperties()
        self.Layout()


    def LoadToolPropertiesByType(self, selection):
        """
        Loads properties by checking what kind of track we have
        """
        #first, unload previous panels
        if self._properties_panel != None:
            self.UnloadToolProperties()
        
        #check if object is track
        if isinstance(selection, model.tracks.Track):

            #check what kind of track object is
            if selection.v1 == Vec3() and selection.v2 == Vec3():
                try:
                    self.LoadToolProperties(self._panels[ID_TRACK_PROPERTIES_STRAIGHT])
                    self._properties_panel.SetTrack(selection)
                    self.TopLevelParent.ChangePaneCaption(self,"Track Properties")
                except KeyError:
                    pass
            else:
                try:
                    self.LoadToolProperties(self._panels[ID_TRACK_PROPERTIES_ARC])
                    self._properties_panel.SetTrack(selection)
                    self.TopLevelParent.ChangePaneCaption(self,"Arc Properties")
                except KeyError:
                    pass
        else:
            try:
                self.LoadToolProperties(self._panels[ID_BASEPOINT_PROPERTIES])
                self.TopLevelParent.ChangePaneCaption(self,"Basepoint Properties")
            except KeyError:
                self.TopLevelParent.ChangePaneCaption(self,"Properties")


    def LoadToolProperties(self, panel):
        """
        Loaded properties panel under the menu.
        """
        
        self._properties_panel = self.GetSizer().Add(panel,1,wx.EXPAND).GetWindow()
        self._properties_panel.Show()
        #Refresh
        self.Layout()
        
    def UnloadToolProperties(self):
        """
        Remove properties panel from sizer and then destroy him
        """
        
        if self.GetSizer().Remove(self._properties_panel):
            self._properties_panel.Hide()
            self._properties_panel = None
            
            #Refresh
            self.Layout()
        
    def OnBaseParametersChange(self):
        if self._properties_panel != None:
            self._properties_panel.OnBaseParametersChange()

    def SetBaseParametersStoreClass(self, store):
        self.param_store = store
        for p in self._panels:
            self._panels[p].SetBaseParametersStoreClass(self.param_store)
        


class BasePointProperties(wx.Panel, PropertiesBaseClass):
    def __init__(self, parent, editor=None, id=wx.ID_ANY):
        wx.Panel.__init__(self, parent, id)
        
        self.Hide()

        s = wx.BoxSizer(wx.VERTICAL)
        self.MakeUI(s)

        self.SetSizer(s)
        #binding events
        self.Bind(wx.EVT_SHOW, self.OnShow)
#        self.Bind(wx.EVT_SPINCTRL, self.OnChange)
        self.Bind(wx.EVT_BUTTON, self.OnChange)        

    def MakeUI(self, s):
        '''
        Angle degrees
        '''
        
        sizer_slider = wx.FlexGridSizer(1,2,5,5)
        
        self.sp_angle = wx.SpinCtrl(self)
        l_angle = wx.StaticText(self,wx.ID_ANY,"Angle (deg)")
        self.sp_angle.SetRange(-360,360) 
               
        sizer_slider.Add(l_angle,0, wx.EXPAND, wx.ALIGN_CENTER)
        sizer_slider.Add(self.sp_angle,1, wx.EXPAND, wx.ALIGN_CENTER)
        
        '''Angle min'''

        self.sp_angle_min = wx.SpinCtrl(self)
        l_angle_min = wx.StaticText(self,wx.ID_ANY,"Angle (min)")
        self.sp_angle_min.SetRange(-100,100)

        sizer_slider.Add(l_angle_min,0, wx.EXPAND, wx.ALIGN_CENTER)
        sizer_slider.Add(self.sp_angle_min,1, wx.EXPAND, wx.ALIGN_CENTER)

        '''Gradient'''

        self.sp_grad = wx.SpinCtrl(self)
        l_grad = wx.StaticText(self,wx.ID_ANY,"Gradient (promiles)")
        self.sp_grad.SetRange(-100,100)

        sizer_slider.Add(l_grad,0, wx.EXPAND, wx.ALIGN_CENTER)
        sizer_slider.Add(self.sp_grad,1, wx.EXPAND, wx.ALIGN_CENTER)

        #making sizer
        s.AddSpacer(5)
        s.Add(sizer_slider)

        self._bOK = wx.Button(self, wx.ID_ANY, "Apply")

        sb = wx.StdDialogButtonSizer()
        sb.AddButton(self._bOK)
        sb.SetAffirmativeButton(self._bOK)
        sb.Realize()

        s.AddSpacer(8)
        s.Add(sb,0,wx.EXPAND)


    def OnShow(self, event):
        """
        Class invoking when show event where arrive
        """
        
        #get basepoint
        editor = self.TopLevelParent.editor
        bp = editor.basePoint        
        #calc deg and min
        main = int(bp.alpha)
        rest = int(bp.alpha * 100) - main * 100
        #setting values
        self.sp_angle.SetValue(bp.alpha)
        self.sp_angle_min.SetValue(rest)
        self.sp_grad.SetValue(bp.gradient)
    
    def OnChange(self, event):

        #get basepoint
        editor = self.TopLevelParent.editor
        bp = editor.basePoint        
        bp.alpha = math.fmod(float(self.sp_angle.GetValue())+360,360.0) + math.fmod(float(self.sp_angle_min.GetValue() / 100.0)+100,100.0)
        bp.gradient = self.sp_grad.GetValue()

        editor.SetBasePoint(bp,True)

#    def SetBaseParametersStoreClass(self, store):
#        """
#        Only for compatybile issues
#        """
#        pass

class TrackPropertiesStraight(wx.Panel, PropertiesBaseClass):
    def __init__(self, parent, editor=None, id = wx.ID_ANY):
        wx.Panel.__init__(self, parent, id)
        
        self.Hide()
        s = wx.BoxSizer(wx.VERTICAL)
        #making layout
        self.MakeUI(s)
        self.BindEvents()
        self.SetSizer(s)

    def SetTrack(self, track):
        #read lenght and angle of track
        length = math.sqrt(math.pow(float(track.p2.x - track.p1.x),2) + math.pow(float(track.p2.y - track.p1.y),2))
#        angle = math.degrees(math.atan2(float(track.p2.x - track.p1.x), float(track.p2.y - track.p1.y)))
#        a1 = track.p1.angleToJUnit()
#        a2 = track.p2.angleToJUnit()
        
        main = length // 1000
        rest = math.fmod(length, 1000)
        self.sl_km.SetValue(main)

        main = rest // 100
        rest = math.fmod(length, 100)
        self.sl_100m.SetValue(main)

        main = rest // 1
        self.sl_1m.SetValue(main)

        #we need this to make changes
        self.track = track


    def MakeUI(self, s):
        """
        Function in wich we make some GUI for changing properties of straight track
        """
        
        '''
        Km slider
        '''
        
        sizer_slider = wx.FlexGridSizer(1,2,5,5)
        self.sl_km = wx.Slider(self,wx.ID_ANY,0,0,10, size=(200,-1), style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        self.sl_km.SetTickFreq(1)
        l_km = wx.StaticText(self,wx.ID_ANY,"Km")
        
        sizer_slider.Add(l_km,0, wx.EXPAND, wx.ALIGN_CENTER)
        sizer_slider.Add(self.sl_km,1, wx.EXPAND, wx.ALIGN_CENTER)
        
        '''
        100 m slider
        '''
        
        self.sl_100m = wx.Slider(self,wx.ID_ANY,0,0,10, size=(200,-1), style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        self.sl_100m.SetTickFreq(1)
        l_100m = wx.StaticText(self,wx.ID_ANY,"100m")
        
        
        sizer_slider.Add(l_100m,0, wx.EXPAND, wx.ALIGN_CENTER)
        sizer_slider.Add(self.sl_100m,1, wx.EXPAND, wx.ALIGN_CENTER)
        
        '''
        1 [m]
        '''
        
        self.sl_1m = wx.Slider(self,wx.ID_ANY,0,0,100, size=(200,-1), style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        self.sl_1m.SetTickFreq(5)
        l_1m = wx.StaticText(self,wx.ID_ANY,"1m")
        
        sizer_slider.Add(l_1m,0, wx.EXPAND, wx.ALIGN_CENTER)
        sizer_slider.Add(self.sl_1m,1, wx.EXPAND, wx.ALIGN_CENTER)

        s.AddSpacer(5)
        s.Add(sizer_slider,0,wx.EXPAND)

        self._bOK = wx.Button(self, wx.ID_ANY, "Apply")

        sb = wx.StdDialogButtonSizer()
        sb.AddButton(self._bOK)
        sb.SetAffirmativeButton(self._bOK)
        sb.Realize()

        s.AddSpacer(8)
        s.Add(sb,0,wx.EXPAND)


    def BindEvents(self):
        """
        Function to bind events with sliders
        """
#        self.Bind(wx.EVT_SCROLL_CHANGED, self.SliderMove)
        self.Bind(wx.EVT_BUTTON, self.SliderMove)        


    def SliderMove(self, event):
        
        if self.sl_km.GetValue() != 0 or self.sl_100m.GetValue() != 0 \
            or self.sl_1m.GetValue() != 0:
            editor = self.TopLevelParent.editor
            bp = editor.basePoint
            point = self.track.nextPoint(bp.point) 
            #change place of basepoint to start of track
            bp.point = point
            #create new track
            new_track = ui.trackfc.TrackFactory().CreateStraight(self.sl_km.GetValue()*1000 + \
                                                                 self.sl_100m.GetValue()*100 + \
                                                                 self.sl_1m.GetValue(), bp)
            #delete old track
            editor.scenery.RemoveRailTracking(self.track)
            #add new
            if new_track.p1 != new_track.p2:
                #new track have length
                editor.scenery.AddRailTracking(new_track)
                editor.SetBasePoint(bp)
                editor.SetSelection(new_track)
            else:
                editor.SetBasePoint(bp)
                editor.SetSelection(None)
                
    
class TrackPropertiesArc(wx.Panel, PropertiesBaseClass):
    def __init__(self, parent, editor=None, id = wx.ID_ANY):
        wx.Panel.__init__(self, parent, id)
        
        self.Hide()
        s = wx.BoxSizer(wx.VERTICAL)
        #making layout
        self.MakeUI(s)
        self.BindEvents()
        self.SetSizer(s)

    def SetTrack(self, track):
        
        #first we calc angle between two vectors
        self.isLeft = False
        a1 = math.degrees(math.atan2(track.v1.x, track.v1.y))
        a2 = math.degrees(math.atan2(-track.v2.x, -track.v2.y))
        
        #we count all to 180 degrees and then take rest of divide to 360 to have
        #good calcs
        x = 180.0 - a1
        a1 = math.fmod(a1+x,360.0)
        a2 = math.fmod(a2+x,360.0)
        
        #if angle of a1 id greater than a2 it means that is left arc
        if a1 > a2:
            angle = a1 - a2
            self.isLeft = True
        else:
            angle = a2 - a1
        #second we calc radius from length of vector
        T = track.v1.length()
        R = T * 3.0 / 4.0 / (math.tan(math.radians(angle) * 0.25))
        
        #calc deg and min
        main = int(angle)
        rest = int(angle * 100) - main * 100
        #setting values
        self.sp_angle.SetValue(main)
        self.sp_angle_min.SetValue(rest)

        self.sp_rad.SetValue(R)

        #we need this to make changes
        self.track = track


    def MakeUI(self, s):
        """
        Function in which we make some GUI for changing properties of straight track
        """
        
        '''
        Angle degrees
        '''
        
        sizer_slider = wx.FlexGridSizer(1,2,5,5)
        
        self.sp_angle = wx.SpinCtrl(self)
        l_angle = wx.StaticText(self,wx.ID_ANY,"Angle (deg)")
        self.sp_angle.SetRange(0,359) 
               
        sizer_slider.Add(l_angle,0, wx.EXPAND | wx.ALIGN_CENTER)
        sizer_slider.Add(self.sp_angle,1, wx.EXPAND | wx.ALIGN_CENTER)
        
        '''Angle min'''

        self.sp_angle_min = wx.SpinCtrl(self)
        l_angle_min = wx.StaticText(self,wx.ID_ANY,"Angle (min)")
        self.sp_angle_min.SetRange(0,100)

        sizer_slider.Add(l_angle_min,0, wx.EXPAND | wx.ALIGN_CENTER)
        sizer_slider.Add(self.sp_angle_min,1, wx.EXPAND | wx.ALIGN_CENTER)

        '''Radius'''

        self.sp_rad = wx.SpinCtrl(self)
        l_rad = wx.StaticText(self,wx.ID_ANY,"Radius (m)")
        self.sp_rad.SetRange(50,25000)

        sizer_slider.Add(l_rad,0, wx.EXPAND | wx.ALIGN_CENTER)
        sizer_slider.Add(self.sp_rad,1, wx.EXPAND | wx.ALIGN_CENTER)        
        
        s.AddSpacer(5)
        s.Add(sizer_slider,0,wx.EXPAND)
        
        self._bOK = wx.Button(self, wx.ID_ANY, "Apply")

        sb = wx.StdDialogButtonSizer()
        sb.AddButton(self._bOK)
        sb.SetAffirmativeButton(self._bOK)
        sb.Realize()

        s.AddSpacer(8)
        s.Add(sb,0,wx.EXPAND)
        
        
    def BindEvents(self):
        """
        Function to bind events with sliders
        """
        self.Bind(wx.EVT_BUTTON, self.OnChange)        


    def OnChange(self, event):
        
        editor = self.TopLevelParent.editor
        bp = editor.basePoint
        point = self.track.nextPoint(bp.point) 
        #change place of basepoint to start of track
        bp.point = point
        v = self.track.getNormalVector(point)
        alpha = math.degrees(math.atan2(v.x, v.y))+180
        bp.alpha = alpha
        #create new track
        angle = math.radians(float(self.sp_angle.GetValue()) + float(self.sp_angle_min.GetValue() / 100.0))
        new_track = ui.trackfc.TrackFactory().CreateArc(angle, self.sp_rad.GetValue(), self.isLeft, bp)
        #delete old track
        editor.scenery.RemoveRailTracking(self.track)
        #add new
        if new_track.p1 != new_track.p2:
            #new track have length
            editor.scenery.AddRailTracking(new_track)
            editor.SetBasePoint(bp)
            editor.SetSelection(new_track)
        else:
            editor.SetBasePoint(bp)
            editor.SetSelection(None)
            
    def SetBaseParametersStoreClass(self, store):
        
        self.param_store = store 
        
    def OnBaseParametersChange(self):
        
        self.sp_rad.SetRange(self.param_store.minR, self.param_store.maxR)
