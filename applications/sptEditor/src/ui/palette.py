"""
Module containing palettes
"""

import os.path
import yaml
import wx



class PaletteFrame(wx.Frame):
    """
    Standalone window for palette.
    """

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, "Palette", \
            style = wx.CAPTION | wx.CLOSE_BOX | wx.RESIZE_BORDER \
                | wx.FRAME_FLOAT_ON_PARENT)
        self.SetMinSize((350, 400))
        self.SetIcons(parent.PrepareApplicationIcons())

        self.palette = TrackPalette(self)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.RestoreFrame()

        self.Layout()
        self.Show(True)


    def OnClose(self, event):
        try:
            self.GetParent().miTogglePalette.Check(False)
            self.StoreFrame()
        finally:
            self.Destroy()


    def RestoreFrame(self):
        config = wx.FileConfig.Get()

        posX = config.ReadInt("/EIFrame/framesPalette/x", 28)
        posY = config.ReadInt("/EIFrame/framesPalette/y", 28)
        width = config.ReadInt("/EIFrame/framesPalette/width", 350)
        height = config.ReadInt("/EIFrame/framesPalette/height", 400)

        self.Move((posX, posY))
        self.SetSize((width, height))


    def StoreFrame(self):
        config = wx.FileConfig.Get()

        pos = self.GetPosition()
        size = self.GetSize()

        config.WriteInt("/EIFrame/framesPalette/x", pos.x)
        config.WriteInt("/EIFrame/framesPalette/y", pos.y)
        config.WriteInt("/EIFrame/framesPalette/width", size.width)
        config.WriteInt("/EIFrame/framesPalette/height", size.height)




class TrackPalette(wx.Panel):
    """
    Track palette
    """

    def __init__(self, parent, id = wx.ID_ANY):
        wx.Panel.__init__(self, parent, id)

        self.LoadPrefabs()
        self.VerifyPrefabs()

        sizerRoot = wx.BoxSizer(wx.VERTICAL)

        searchPanel = wx.Panel(self, wx.ID_ANY)
        sizerSearch = wx.BoxSizer(wx.HORIZONTAL)
        sizerSearch.Add(wx.StaticText(searchPanel, wx.ID_ANY, label="Search:"), \
            0, wx.SHAPED | wx.ALIGN_CENTER)

        self.searchTextCtrl = wx.TextCtrl(searchPanel, wx.ID_ANY)
        self.searchTextCtrl.SetMaxLength(32)

        sizerSearch.Add(self.searchTextCtrl, 3, wx.EXPAND)

        self.clearSearch = wx.Button(searchPanel, wx.ID_CLEAR)
        self.clearSearch.Bind(wx.EVT_BUTTON, self.OnClearSearch, id=wx.ID_CLEAR)

        sizerSearch.Add(self.clearSearch, 1, wx.EXPAND)
        searchPanel.SetSizer(sizerSearch)

        sizerPalette = wx.BoxSizer(wx.VERTICAL)
        palettePanel = wx.Panel(self, wx.ID_ANY, style = wx.BORDER_SUNKEN)
        for trackingType in self.prefabs.keys():
            groupPanel = wx.Panel(palettePanel, wx.ID_ANY)
            groupSizer = wx.BoxSizer(wx.VERTICAL)

            itemContainerPanel = wx.ScrolledWindow(groupPanel, wx.ID_ANY, \
                name=trackingType, style = wx.HSCROLL | wx.BORDER_SIMPLE)
            itemContainerSizer = wx.BoxSizer(wx.VERTICAL)

            for e in self.prefabs[trackingType]:
                itemPanel = wx.Panel(itemContainerPanel, wx.ID_ANY, name=e.label)
                itemSizer = wx.BoxSizer(wx.HORIZONTAL)

                itemLabel = wx.StaticText(itemPanel, wx.ID_ANY, label=e.label)
                itemSizer.Add(itemLabel, 1, wx.EXPAND | wx.ALIGN_CENTER)

                handlesPanel = wx.Panel(itemPanel, wx.ID_ANY)
                handlesSizer = wx.BoxSizer(wx.HORIZONTAL)
                ## Handles
                for h in e.handles:
                    hButton = wx.BitmapButton(handlesPanel, wx.ID_ANY)
                    bitmapPath = os.path.join("icons", "actions", h[1]) + ".png"
                    hButton.SetBitmapLabel(wx.Bitmap(bitmapPath))
                    handlesSizer.Add(hButton, 0, wx.SHAPED)
                
                handlesPanel.SetSizer(handlesSizer)

                itemSizer.Add(handlesPanel, 1, wx.EXPAND)

                itemPanel.SetSizer(itemSizer)
                itemContainerSizer.Add(itemPanel, 0, wx.EXPAND)

            itemContainerPanel.SetSizer(itemContainerSizer)
            itemContainerSizer.FitInside(itemContainerPanel)
            itemContainerPanel.EnableScrolling(False, True)
            itemContainerPanel.SetVirtualSizeHints(300, 50)

            expanderButton = wx.Button(groupPanel, wx.ID_ANY, name="eb_" + trackingType)
            expanderButton.SetLabel("%s <<" % trackingType)
            expanderButton.Bind(wx.EVT_BUTTON, self.OnExpandButton, id=wx.ID_ANY)
            
            groupSizer.Add(expanderButton, 0, wx.EXPAND)
            groupSizer.Add(itemContainerPanel, 0, wx.EXPAND | wx.ALL, 2)
            groupPanel.SetSizer(groupSizer)

            sizerPalette.Add(groupPanel, 0, wx.EXPAND)

        palettePanel.SetSizer(sizerPalette)

        sizerRoot.Add(searchPanel, 0, wx.EXPAND | wx.ALL, 5)
        sizerRoot.Add(palettePanel, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizerRoot)
        sizerRoot.Fit(self)


    def LoadPrefabs(self):
        self.prefabs = yaml.load(file("prefabric.yaml", "r"))


    def VerifyPrefabs(self):
        for v in self.prefabs.values():
            for e in v:
                if not e.Verify():
                    raise ValueError, "%s is invalid palette item" % e


    def OnExpandButton(self, event):
        button = event.GetEventObject()
        label = button.GetLabel()[:-3]
        panel = button.GetParent()
        sizer = panel.GetSizer()
        if sizer.IsShown(1):
            sizer.Hide(1, True)
            label = label + " >>"
        else:
            sizer.Show(1, True)
            label = label + " <<"
        button.SetLabel(label)
        sizer.Layout()
        panel.GetParent().GetSizer().Layout()


    def OnClearSearch(self, event):
        self.searchTextCtrl.Clear()
        self.searchTextCtrl.SetFocus()
        # Show all hidden fields



class TrackingItem:
    """
    An item of track palette.
    """

    """
    Textual description - searchable
    """
    description = dict()
    """
    List of handles. Each element is a tuple of
    Vec3 and the icon description
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

