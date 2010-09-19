"""
Module containing palettes
"""

import os.path
import yaml
import wx

import Application
import model.tracks
import ui.dialog
import ui.trackfc
import wx.glcanvas



class TrackPalette(wx.Panel):
    """
    Track palette
    """

    def __init__(self, parent, id = wx.ID_ANY, w=400, h=400):
        wx.Panel.__init__(self, parent, id, wx.DefaultPosition,wx.Size(w,h),style = wx.WANTS_CHARS | wx.FULL_REPAINT_ON_RESIZE)

        self.LoadPrefabs()
        self.VerifyPrefabs()

        sizerRoot = wx.BoxSizer(wx.VERTICAL)

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

        self.sizerPalette = wx.BoxSizer(wx.VERTICAL)
        palettePanel = wx.Panel(self, wx.ID_ANY, style = wx.BORDER_SUNKEN)

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

        self.groups = [straightGroup, arcGroup, lSwitchGroup, rSwitchGroup]

        palettePanel.SetSizer(self.sizerPalette)

        sizerRoot.Add(searchPanel, 0, wx.EXPAND | wx.ALL, 5)
        sizerRoot.Add(palettePanel, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizerRoot)
        sizerRoot.Fit(self)

#        self.Bind(wx.EVT_CLOSE, self.OnClose)
#        self.Bind(wx.EVT_DESTROY, self.OnClose)

    def OnClose(self):
        self.Parent.miTogglePalette.Check(False)
        print "Palette on Close"

    def LoadPrefabs(self):
        self.prefabs = yaml.load(file("prefabric.yaml", "r"))


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
    Panel grouping rail tracking type.
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

