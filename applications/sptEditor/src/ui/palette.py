"""
Module containing palettes
"""

import os.path
import sys
import yaml
import wx

import Application
import model.tracks
import ui.dialog
import ui.trackfc
import sptyaml

import ui.flatmenu as FM
from wx.lib.agw.artmanager import ArtManager
#from wx.lib.agw.fmresources import ControlFocus, ControlPressed
from wx.lib.agw.fmresources import FM_OPT_SHOW_TOOLBAR, FM_OPT_MINIBAR, FM_OPT_IS_LCD

from ui.uitools import ResizeBitmap #, FindItemById, SelectButton, DeselectButton 

#from ui.toolbar import ID_INSERT_TRACK, ID_INSERT_CURVE, ID_INSERT_SWITCH

#from Application import ID_TRACK_TOOL, ID_SWITCH_TOOL
ID_TRACK_TOOL = 1
ID_SWITCH_TOOL = 2
ID_TRACK_TOOL_LEFT = 0
ID_TRACK_TOOL_STRAIGHT = 1
ID_TRACK_TOOL_RIGHT = 2

class ToolsPalette(wx.Panel):
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



class PropertiesPalette(wx.ScrolledWindow):
    """
    Base class for all properties palettes for tools
    """
    def __init__(self, parent, id = wx.ID_ANY, w=200, h=400):
        wx.ScrolledWindow.__init__(self, parent, id)
        self.SetSizer(wx.BoxSizer(wx.VERTICAL))

        self._panels = {
                        }    

    def LoadToolProperties(self, panel):
        """
        Loaded properties panel under the menu.
        """
        
        self._properties_panel = self.GetSizer().Add(panel(self),1,wx.EXPAND).GetWindow()
        
        #Refresh
        self.Layout()
        
    def UnloadToolProperties(self):
        """
        Remove properties panel from sizer and then destroy him
        """
        
        if self.GetSizer().Remove(self._properties_panel):
            self._properties_panel.Destroy()
            self._properties_panel = None
            
            #Refresh
            self.Layout()
        

class TrackTool(wx.Panel):
    def __init__(self, parent, id = wx.ID_ANY):
        wx.Panel.__init__(self, parent, id)

        #self.searchTextCtrl = wx.TextCtrl(self, wx.ID_ANY)
      
        #wx.SpinCtrl(self)
        s = wx.BoxSizer(wx.VERTICAL)
        #s.Add(self._menu, 0, wx.EXPAND)
        self._rb = wx.RadioBox(self,wx.ID_ANY,"Direction",style=wx.RA_SPECIFY_COLS,majorDimension=3, \
                          choices=["Left","Straight","Right"], size=wx.Size(-1,50) \
                          )
        
        
        self.Bind(wx.EVT_RADIOBOX, self.ChangedDirectionOfTrack)
        self._tool_panel = None

        self.tools = {
                      ID_TRACK_TOOL_STRAIGHT: self.LoadStraightTrackPalette
                      }
        
        s.Add(self._rb,0,wx.SHAPED, wx.ALIGN_CENTER)
        
        self.SetSizer(s)
        
        self._rb.SetSelection(1)
        self.ChangedDirectionOfTrack(None)
       
    def ChangedDirectionOfTrack(self, event):
        """
        Function that is called within tool selected radio buttons in menu.
        It bind id of button with appriopriate Tools panel to load.
        Bind is stored in tools variable
        """
        
        if self._tool_panel != None:
            self.UnloadToolPanel()
        
        try:
            self._tool_panel = self.GetSizer().Add(self.tools[self._rb.GetSelection()]())
        except KeyError:   
            pass 
        self.Layout()
        
    def UnloadToolPanel(self):
        """
        Remove tools panel from sizer and then destroy him
        """
        
        if self.GetSizer().Remove(self._tool_panel):
            #self._tool_panel.Destroy()
            self._tool_panel = None
            
            #Refresh
            self.Layout()
    
    def LoadStraightTrackPalette(self):
            
        '''
        Km slider
        '''
        
        sizer_slider = wx.FlexGridSizer(1,2,5,5)
        #sizer_slider_km = wx.BoxSizer(wx.HORIZONTAL)
        sl_km = wx.Slider(self,wx.ID_ANY,0,0,10, size=(200,-1), style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        sl_km.SetTickFreq(1)
        l_km = wx.StaticText(self,wx.ID_ANY,"Km")
        
        #sizer_slider_km.Add(l_km,0,wx.SHAPED, wx.RIGHT)
        #sizer_slider_km.Add(sl_km,1,wx.SHAPED)
        
        sizer_slider.Add(l_km,0, wx.SHAPED, wx.ALIGN_CENTER)
        sizer_slider.Add(sl_km,1, wx.SHAPED, wx.ALIGN_CENTER)
        
        '''
        100 m slider
        '''
        
        #sizer_slider_100m = wx.BoxSizer(wx.HORIZONTAL)
        sl_100m = wx.Slider(self,wx.ID_ANY,0,0,10, size=(200,-1), style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        sl_100m.SetTickFreq(1)
        l_100m = wx.StaticText(self,wx.ID_ANY,"100m")
        
        #sizer_slider_100m.Add(l_100m,0,wx.SHAPED, wx.ALIGN_CENTER_VERTICAL)
        #sizer_slider_100m.Add(sl_100m,1,wx.SHAPED)
        
        sizer_slider.Add(l_100m,0, wx.SHAPED, wx.ALIGN_CENTER)
        sizer_slider.Add(sl_100m,1, wx.SHAPED, wx.ALIGN_CENTER)
        '''
        1 [m]
        '''
        
        #sizer_slider_1m = wx.BoxSizer(wx.HORIZONTAL)
        sl_1m = wx.Slider(self,wx.ID_ANY,0,0,100, size=(200,-1), style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        sl_1m.SetTickFreq(5)
        l_1m = wx.StaticText(self,wx.ID_ANY,"1m")
        
        #sizer_slider_1m.Add(l_1m,0,wx.SHAPED, wx.ALIGN_CENTER_VERTICAL)
        #sizer_slider_1m.Add(sl_1m,1,wx.SHAPED)
        sizer_slider.Add(l_1m,0, wx.SHAPED, wx.ALIGN_CENTER)
        sizer_slider.Add(sl_1m,1, wx.SHAPED, wx.ALIGN_CENTER)
        
        #self.GetSizer().Add(sizer_slider,0,wx.EXPAND)
        return sizer_slider


class TrackToolStraight(wx.Panel):
    def __init__(self, parent, id = wx.ID_ANY):
        wx.Panel.__init__(self, parent, id)
        
        
        s = wx.BoxSizer(wx.VERTICAL)
        '''
        Km slider
        '''
        
        sizer_slider = wx.FlexGridSizer(1,2,5,5)
        #sizer_slider_km = wx.BoxSizer(wx.HORIZONTAL)
        sl_km = wx.Slider(self,wx.ID_ANY,0,0,10, size=(200,-1), style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        sl_km.SetTickFreq(1)
        l_km = wx.StaticText(self,wx.ID_ANY,"Km")
        
        #sizer_slider_km.Add(l_km,0,wx.SHAPED, wx.RIGHT)
        #sizer_slider_km.Add(sl_km,1,wx.SHAPED)
        
        sizer_slider.Add(l_km,0, wx.SHAPED, wx.ALIGN_CENTER)
        sizer_slider.Add(sl_km,1, wx.SHAPED, wx.ALIGN_CENTER)
        
        '''
        100 m slider
        '''
        
        #sizer_slider_100m = wx.BoxSizer(wx.HORIZONTAL)
        sl_100m = wx.Slider(self,wx.ID_ANY,0,0,10, size=(200,-1), style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        sl_100m.SetTickFreq(1)
        l_100m = wx.StaticText(self,wx.ID_ANY,"100m")
        
        #sizer_slider_100m.Add(l_100m,0,wx.SHAPED, wx.ALIGN_CENTER_VERTICAL)
        #sizer_slider_100m.Add(sl_100m,1,wx.SHAPED)
        
        sizer_slider.Add(l_100m,0, wx.SHAPED, wx.ALIGN_CENTER)
        sizer_slider.Add(sl_100m,1, wx.SHAPED, wx.ALIGN_CENTER)
        '''
        1 [m]
        '''
        
        #sizer_slider_1m = wx.BoxSizer(wx.HORIZONTAL)
        sl_1m = wx.Slider(self,wx.ID_ANY,0,0,100, size=(200,-1), style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        sl_1m.SetTickFreq(5)
        l_1m = wx.StaticText(self,wx.ID_ANY,"1m")
        
        #sizer_slider_1m.Add(l_1m,0,wx.SHAPED, wx.ALIGN_CENTER_VERTICAL)
        #sizer_slider_1m.Add(sl_1m,1,wx.SHAPED)
        sizer_slider.Add(l_1m,0, wx.SHAPED, wx.ALIGN_CENTER)
        sizer_slider.Add(sl_1m,1, wx.SHAPED, wx.ALIGN_CENTER)


        s.Add(sizer_slider)
        self.SetSizer()









        
class TrackPalette(wx.ScrolledWindow):
    """
    Base class for palette with buttons to quick inserting buttons in editor
    """

    def __init__(self, parent, id = wx.ID_ANY, w=200, h=400):
        wx.ScrolledWindow.__init__(self, parent, id,)

        #self.SetSize(wx.Size(w,h))
        #Loading prefabs of tracks from prefabric.yaml file using sptLoader (sptyaml.py file)
        self.LoadPrefabs()
        #Verify loaded tracks
        self.VerifyPrefabs()
        
        #adding main sizer in form
        sizerRoot = wx.BoxSizer(wx.VERTICAL)
        
        #adding search pole on top of pallete
        searchPanel = wx.Panel(self, wx.ID_ANY)
        sizerSearch = wx.BoxSizer(wx.HORIZONTAL)
        sizerSearch.Add(wx.StaticText(searchPanel, wx.ID_ANY, label="Search:"), \
            0, wx.SHAPED | wx.ALIGN_CENTER)

        self.searchTextCtrl = wx.TextCtrl(searchPanel, wx.ID_ANY)
        self.searchTextCtrl.SetMaxLength(32)
        self.searchTextCtrl.SetFocus()

        self.searchTextCtrl.Bind(wx.EVT_TEXT, self.OnTextSearch, id=wx.ID_ANY)

        sizerSearch.Add(self.searchTextCtrl, 3, wx.EXPAND)

        self.clearSearch = wx.Button(searchPanel, wx.ID_CLEAR)
        self.clearSearch.Bind(wx.EVT_BUTTON, self.OnClearSearch, id=wx.ID_CLEAR)

        sizerSearch.Add(self.clearSearch, 1, wx.EXPAND)
        searchPanel.SetSizer(sizerSearch)

        #adding sizer for track groups below search
        self.sizerPalette = wx.BoxSizer(wx.VERTICAL)
        palettePanel = wx.Panel(self, wx.ID_ANY, style = wx.BORDER_SUNKEN)
        
        #Create new groups for everyone type of tracks
        # Straight
        straightGroup = TrackingTypeGroup(palettePanel, 'Straight', self.prefabs['straight'])
        self.sizerPalette.Add(straightGroup, 0, wx.EXPAND)

        # Arcs
        arcGroup = TrackingTypeGroup(palettePanel, 'Arcs', self.prefabs['arcs'])
        self.sizerPalette.Add(arcGroup, 0, wx.EXPAND)

        # Left switches
        lSwitchGroup = TrackingTypeGroup(palettePanel, 'Left switches', self.prefabs['left_switches'])
        self.sizerPalette.Add(lSwitchGroup, 0, wx.EXPAND)

        # Right switches
        rSwitchGroup = TrackingTypeGroup(palettePanel, 'Right switches', self.prefabs['right_switches'])
        self.sizerPalette.Add(rSwitchGroup, 0, wx.EXPAND)

        #collate created  groups into dictionary
        self.groups = [straightGroup, arcGroup, lSwitchGroup, rSwitchGroup]

        palettePanel.SetSizer(self.sizerPalette)

        sizerRoot.Add(searchPanel, 0, wx.EXPAND | wx.ALL, 5)
        sizerRoot.Add(palettePanel, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizerRoot)
        sizerRoot.Fit(self)

#        self.Bind(wx.EVT_CLOSE, self.OnClose)
#        self.Bind(wx.EVT_DESTROY, self.OnClose)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouse)
        self.SetScrollRate(10,15)

    def OnMouse(self, event):
        print "Track panel mouse wheel "+event.GetWheelRotation()

    def OnClose(self):
        self.Parent.miTogglePalette.Check(False)
        
    def LoadPrefabs(self):
        """
        Method only for loading prefabs to memory using SPT own loader
        """
        self.prefabs = yaml.load(file("prefabric.yaml", "r"), sptyaml.SptLoader)
        
    def VerifyPrefabs(self):
        for v in self.prefabs.values():
            for e in v:
                if not e.Verify():
                    raise ValueError, "%s is invalid palette item" % e


    def OnClearSearch(self, event):
        self.searchTextCtrl.Clear()
        self.searchTextCtrl.SetFocus()


    def OnTextSearch(self, event):
        exp = event.GetEventObject().GetValue()
        if exp.strip() == "":
            self.ClearSearch()
        else:
            self.Search(exp)


    def ClearSearch(self):
        for g in self.groups:
            g.ClearSearch()
        self.sizerPalette.Layout()


    def Search(self, exp):
        for g in self.groups:
            g.Search(exp)
        self.sizerPalette.Layout()




class TrackingTypeGroup(wx.Panel):
    """
    Panel grouping rail tracking category.
    """

    def __init__(self, parent, label, elements):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self.label = label

        sizer = wx.BoxSizer(wx.VERTICAL)

        itemContainerPanel = wx.ScrolledWindow(self, wx.ID_ANY, \
                style = wx.HSCROLL | wx.BORDER_SIMPLE)
        itemContainerSizer = wx.BoxSizer(wx.VERTICAL)

        self.rows = []

        for elem in elements:
            row = TrackingItemRow(itemContainerPanel, elem)
            itemContainerSizer.Add(row, 0, wx.EXPAND)
            self.rows.append(row)

        itemContainerPanel.SetSizer(itemContainerSizer)
        #itemContainerPanel.SetVirtualSizeHints(300, 50)
        itemContainerPanel.FitInside()
        #itemContainerPanel.SetScrollRate(-1, 50)

        self.expanderButton = wx.Button(self, wx.ID_ANY)
        self.expanderButton.SetLabel("%s <<" % label)
        self.expanderButton.Bind(wx.EVT_BUTTON, self.OnExpand, id=wx.ID_ANY)
            
        sizer.Add(self.expanderButton, 0, wx.EXPAND)
        sizer.Add(itemContainerPanel, 0, wx.EXPAND | wx.ALL, 2)
        self.SetSizer(sizer)


    def OnExpand(self, event):
        sizer = self.GetSizer()
        if sizer.IsShown(1):
            sizer.Hide(1, True)
            label = self.label + " >>"
        else:
            sizer.Show(1, True)
            label = self.label + " <<"
        self.expanderButton.SetLabel(label)
        sizer.Layout()
        self.GetParent().GetSizer().Layout()


    def ClearSearch(self):
        for row in self.rows:
            row.ClearSearch()
        if not self.IsShown():
            self.Show(True)


    def Search(self, exp):
        visible = 0
        for row in self.rows:
            if row.Search(exp):
                visible = visible + 1
        self.Show(visible != 0)




class TrackingItemRow(wx.Panel):
    """
    A row that contains palette item.
    """

    def __init__(self, parent, item):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY)
        self.item = item

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        itemLabel = wx.StaticText(self, wx.ID_ANY, label=item.label)
        sizer.Add(itemLabel, 1, wx.EXPAND | wx.ALIGN_CENTER)

        handlesPanel = wx.Panel(self, wx.ID_ANY)
        handlesSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Handles
        for h in item.handles:
            hButton = TrackingHandleButton(handlesPanel, h[0], h[1])
            handlesSizer.Add(hButton, 0, wx.SHAPED)
                
        handlesPanel.SetSizer(handlesSizer)
        sizer.Add(handlesPanel, 1, wx.EXPAND)

        self.SetSizer(sizer)


    def ClearSearch(self):
        if not self.IsShown():
            self.Show(True)


    def Search(self, exp):
        match = False
        exps = exp.lower().split("*")
        for e in exps:
            if self.item.label.lower().find(e) != -1:
                match = True
        self.Show(match)
        return match
        



class TrackingHandleButton(wx.BitmapButton):
    """
    Bitmap button with handle
    """

    def __init__(self, parent, point, iconName):
        wx.BitmapButton.__init__(self, parent, id=wx.ID_ANY, size=(32, 32))
        bitmapPath = os.path.join("icons", "actions", iconName) + ".png"
        self.SetBitmapLabel(wx.Bitmap(bitmapPath))
        self.point = point

        self.editor = None

        self.Bind(wx.EVT_BUTTON, self.OnHandle, id=wx.ID_ANY)


    def GetRailTracking(self):
        return self.GetParent().GetParent().item.railTracking


    def GetEditor(self):
        if self.editor == None:
            # Cache reference
            self.editor = wx.FindWindowById(Application.ID_EDITOR)
        return self.editor


    def OnHandle(self, event):
        template = self.GetRailTracking()
        editor = self.GetEditor()

        name = None
        if not isinstance(template, model.tracks.Track):
            #print "Request for name!"
            nameDialog = ui.dialog.NameDialog(wx.FindWindowById(Application.ID_MAIN_FRAME))
            ret = nameDialog.ShowModal()
            if ret != wx.ID_OK:
                return
            name = nameDialog.GetName()

        tf = ui.trackfc.TrackFactory(editor)
        rail = tf.CopyRailTracking(template, self.point)
        rail.name = name

        editor.scenery.AddRailTracking(rail)




class TrackingItem:
    """
    An item of track palette.
    """

    """
    Textual description
    """
    description = dict()
    """
    List of handles. Each element is a tuple of
    Vec3 and the standarized handle icon name
    """
    handles = list()
    """
    Rail tracking to insert
    """
    railTracking = None
    """
    Label presented on UI
    """
    label = None

    def __init__(self):
        pass


    def __repr__(self):
        return self.label 


    def Verify(self):
        for p in map(lambda h: h[0], self.handles):
            if not self.railTracking.containsPoint(p):
                return False
        return True

