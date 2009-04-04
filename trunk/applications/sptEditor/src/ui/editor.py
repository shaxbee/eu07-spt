"""
Module containing main UI classes of scenery editor control.

@author adammo
"""

import datetime
import logging

import wx

import model.tracks
import ui.views

SCALE_FACTOR = 1000.0


class SceneryEditor(wx.Panel):
    """
    Scenery editor control.
    """

    def __init__(self, parent, id = wx.ID_ANY):
        wx.Panel.__init__(self, parent, id, style = wx.BORDER_SUNKEN)
        
        sizer = wx.FlexGridSizer(2, 2, 1, 1)

        corner = wx.Panel(self, name = "Corner")
        corner.SetBackgroundColour('WHITE')
        self.leftRuler = Ruler(self, orientation = wx.VERTICAL, \
            name = "Left ruler")
        self.topRuler = Ruler(self, orientation = wx.HORIZONTAL, \
            name = "Top ruler")
        self.parts = [PlanePart(self)]

        sizer.Add(corner)
        sizer.Add(self.topRuler, flag = wx.LEFT | wx.EXPAND)
        sizer.Add(self.leftRuler, flag = wx.TOP | wx.EXPAND)
        sizer.Add(self.parts[0], 1, wx.EXPAND | wx.ALL)
        sizer.AddGrowableCol(1, 1)
        sizer.AddGrowableRow(1, 1)
        
        self.SetSizer(sizer)


    def SetScenery(self, scenery):
        """
        Sets the scenery. Notify also active parts.
        """
        self.scenery = scenery
        for part in self.parts:
            part.SetScenery(scenery)



class PlanePart(wx.ScrolledWindow):
    """
    Editor Part displaying XZ view of scenery.
    """

    def __init__(self, parent, id = wx.ID_ANY):
        wx.ScrolledWindow.__init__(self, parent, id, \
            style = wx.VSCROLL | wx.HSCROLL)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOTION, self.OnMoveUpdateStatusBar)
        self.Bind(wx.EVT_SCROLLWIN, parent.topRuler.HandleOnScroll)
        self.Bind(wx.EVT_SCROLLWIN, parent.leftRuler.HandleOnScroll)

        self.logger = logging.getLogger('Paint')

        self.scale = 400.0

        self.minX = -1000.0
        self.minZ = -1000.0
        self.maxX = 1000.0
        self.maxZ = 1000.0

        self.extentX = 0
        self.extentY = 0
        
        self.trackCache = []
        self.switchCache = []
        
        size = self.ComputePreferredSize() 
        self.SetVirtualSize(size)
        self.SetupScrolling()
        
        
    def SetScenery(self, scenery):
        self.trackCache = []
        self.switchCache = []
        for element in scenery.RailTrackingIterator():
            self.__AddView(element)
            
        self.ComputeMinMax(True)
        self.Refresh()


    def __AddView(self, element):
        if isinstance(element, model.tracks.Track):
            self.trackCache.append(ui.views.TrackView(element))
        elif isinstance(element, model.tracks.Switch):
            self.switchCache.append(ui.views.RailSwitchView(element))
        else:
            raise ValueError("Unsupported element: " + str(type(element)))
        

    def ComputeMinMax(self, doScaling = False):
        """
        Computes bounds of scenery expressed in scenery coordinates.
        """
        nMinX = -1000.0
        nMinZ = 1000.0
        nMaxX = -1000.0
        nMaxZ = 1000.0

        # tracks
        for v in self.trackCache:
            (vMinX, vMaxX, vMinZ, vMaxZ) = v.GetMinMax()
            nMinX = min(vMinX, nMinX)
            nMaxX = max(vMaxX, nMaxX)
            nMinZ = min(vMinZ, nMinZ)
            nMaxZ = max(vMaxZ, nMaxZ)
        # switches
        for v in self.switchCache:
            (vMinX, vMaxX, vMinZ, vMaxZ) = v.GetMinMax()
            nMinX = min(vMinX, nMinX)
            nMaxX = max(vMaxX, nMaxX)
            nMinZ = min(vMinZ, nMinZ)
            nMaxZ = max(vMaxZ, nMaxZ)
        # base point

        # Changes
        if doScaling or nMinX < self.minX or nMinZ < self.minZ \
            or nMaxX > self.maxX or nMaxZ > self.maxZ:
            self.minX = min(self.minX, nMinX)
            self.minZ = min(self.minZ, nMinZ)
            self.maxX = max(self.maxX, nMaxX)
            self.maxZ = max(self.maxZ, nMaxZ)

            self.__ScaleAll(self.scale)

            return True
        else:
            return False


    def GetScale(self):
        return self.scale


    def SetScale(self, scale):
        self.scale = scale
        self.SetVirtualSize(self.ComputePreferredSize())
        self.__ScaleAll(scale)
        self.Update()
        self.Refresh()
        self.GetParent().topRuler.Refresh()
        self.GetParent().leftRuler.Refresh()
        
        
    def __ScaleAll(self, scale):
        for v in self.trackCache:
            v.Scale(scale, self.minX, self.maxX, self.minZ, self.maxZ)
        for v in self.switchCache:
            v.Scale(scale, self.minX, self.maxX, self.minZ, self.maxZ)


    def ViewToModel(self, point):
        """
        Converts 2D point of UI editor coordinates into 3D point
        of scenery coordinates.
        """
        p3d = (float((point[0]-100)/self.scale * SCALE_FACTOR + self.minX), \
            0.0,
            -float((point[1]-100)/self.scale * SCALE_FACTOR + self.minZ))
        return p3d


    def ModelToView(self, point):
        """
        Converts 3D point of scenery coordiante into 2D point of
        UI editor coordinates.
        """        
        p2d = (int((point[0] - self.minX) * self.scale / SCALE_FACTOR + 100), \
            int((-point[2] - self.minZ) * self.scale / SCALE_FACTOR + 100))
        return p2d


    def CenterViewAt(self, x, y):
        """
        Centers the view on following component point.
        """
        (pw, ph) = self.GetVirtualSize()
        (vw, vh) = self.GetSize()
        (ux, uy) = self.GetScrollPixelsPerUnit()
        x = x - vw / 2
        y = y - vh / 2
        x = max(0, x)
        x = min(x, pw - vw)
        y = max(0, y)
        y = min(y, ph - vh)
        self.Scroll(x / ux, y / uy)
        # Update rulers
        self.GetParent().leftRuler.Refresh()
        self.GetParent().topRuler.Refresh()


    def OnSize(self, event):

        self.Refresh()


    def ComputePreferredSize(self):
        (w, h) = self.GetSize()
        
        return (max(w, int(self.scale * (self.maxX - self.minX) \
                / SCALE_FACTOR) + 200) + self.extentX,
            max(h + self.extentY, int(self.scale * (self.maxZ - self.minZ) \
               / SCALE_FACTOR) + 200) + self.extentY)


    def SetupScrolling(self):
        """
        Sets up scrolling of the window.
        """
        self.SetScrollRate(20, 20)
        


    def OnPaint(self, event):

        dc = wx.PaintDC(self)
        self.DoPrepareDC(dc)

        clip = self.GetUpdateRegion().GetBox()
        (clip.x, clip.y) = self.CalcUnscrolledPosition(clip.x, clip.y)

        startTime = datetime.datetime.now()
        try:
            self.PaintBackground(dc, clip)
            self.PaintForeground(dc, clip)
        finally:
            delta = datetime.datetime.now() - startTime
            idelta = delta.days * 86400 + delta.seconds * 1000000 \
                + delta.microseconds
            self.logger.debug(u"Paint lasted %d \u00b5s" % idelta)


    def PaintBackground(self, dc, clip):
        """
        Paints part background.
        """
        self.PaintGrid(dc, clip)


    def PaintGrid(self, dc, clip):
        """
        Paints grid.
        """
        self.PaintAuxiliaryGrid(dc, clip)
        self.PaintMinMaxBounds(dc, clip)


    def PaintAuxiliaryGrid(self, dc, clip):
        """
        Paints a grid.
        """
        center2D = self.ModelToView((0.0, 0.0, 0.0))

        xoffset = clip.x + clip.width
        yoffset = clip.y + clip.height

        oldPen = dc.GetPen()
        dc.SetPen(wx.Pen('#666666'))
        try:
            x = center2D[0]
            while x > clip.x:
                x = x - 100
                dc.DrawLine(x, clip.y, x, yoffset)
            x = center2D[0]
            while x < xoffset:
                dc.DrawLine(x, clip.y, x, yoffset)
                x = x + 100
        
            y = center2D[1]
            while y > clip.y:
                y = y - 100
                dc.DrawLine(clip.x, y, xoffset, y)
            y = center2D[1]
            while y < yoffset:
                dc.DrawLine(clip.x, y, xoffset, y)
                y = y + 100
        finally:
            dc.SetPen(oldPen)

        oldPen = dc.GetPen()
        dc.SetPen(wx.Pen('#ff0000'))
        try:
            dc.DrawPoint(center2D[0], center2D[1])
        finally:
            dc.SetPen(oldPen)


    def PaintMinMaxBounds(self, dc, clip):
        """
        Paints the borders around min/max.
        """
        x = int((self.maxX - self.minX) * self.scale / SCALE_FACTOR) + 100
        y = int((self.maxZ - self.minZ) * self.scale / SCALE_FACTOR) + 100

        oldPen = dc.GetPen()
        dc.SetPen(wx.Pen("#999999"))
        try:
            dc.DrawLine(clip.x, 100, clip.x + clip.width, 100)

            dc.DrawLine(x, clip.y, x, clip.y + clip.height)

            dc.DrawLine(clip.x, y, clip.x + clip.width, y)

            dc.DrawLine(100, clip.y, 100, clip.y + clip.height)
        finally:
            dc.SetPen(oldPen)


    def PaintForeground(self, dc, clip):
        """
        Paints foreground
        """
        self.PaintTracks(dc, clip)
        self.PaintSwitches(dc, clip)
        self.PaintScale(dc, clip)
        
        
    def PaintTracks(self, dc, clip):
        """
        Paint rail tracks.
        """
        oldPen = dc.GetPen()
        try:
            dc.SetPen(wx.Pen((34, 139, 34), 3))
            for v in self.trackCache:
                v.Draw(dc, clip)
        finally:
            dc.SetPen(oldPen)
            
            
    def PaintSwitches(self, dc, clip):
        """
        Paints rail switches.
        """
        oldPen = dc.GetPen()
        try:
            dc.SetPen(wx.Pen((255, 153, 153), 3))
            for v in self.switchCache:
                v.Draw(dc, clip)
        finally:
            dc.SetPen(oldPen)


    def PaintScale(self, dc, clip):
        """
        Paints a scale.
        """

        # TODO: Draw scale in upper, right corner

        dc.DrawText("%.2f" % self.scale, 5, 5)


    def OnMoveUpdateStatusBar(self, event):
        """
        Updates 3D coordinates in case of mouse movement on frame status bar.
        """
        opoint = event.GetPosition()
        point = self.CalcUnscrolledPosition(event.GetPosition())
        (a, b, c) = self.ViewToModel(point)

        bar = self.GetParent().GetParent().GetStatusBar()
        bar.SetStatusText("%.3f, %.3f, %.3f" % (a, b, c))

        self.GetParent().topRuler.UpdateMousePointer(opoint)
        self.GetParent().leftRuler.UpdateMousePointer(opoint)




class Ruler(wx.Control):
    """
    A ruler for scenery editor.
    """

    def __init__(self, parent, orientation, id = wx.ID_ANY, name = None):
        wx.Window.__init__(self, parent, id = id, name = name)
        self.SetBackgroundColour((255, 220, 153))
        self.SetMinSize((24, 24))

        self.orientation = orientation

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.offset = 0
        self.pick = None


    def OnSize(self, event):        
        """
        Refresh.
        """
        self.Refresh()


    def OnPaint(self, event):
        """
        Paints a control.
        """
        dc = wx.PaintDC(self)
        clip = self.GetUpdateRegion().GetBox()

        self.PaintScale(dc, clip)
        self.PaintMousePointer(dc, clip)


    def PaintScale(self, dc, clip):
        """
        Paints scale.
        """
        oldPen = dc.GetPen()
        oldTextFg = dc.GetTextForeground()
        oldFont = dc.GetFont()
        try:
            dc.SetPen(wx.Pen((0, 51, 153)))
            dc.SetTextForeground((0, 51, 153))
            dc.SetFont(wx.Font(8, wx.SWISS, wx.FONTSTYLE_NORMAL, \
                wx.FONTWEIGHT_NORMAL))

            part = self.GetParent().parts[0]
            (unitX, unitZ) = part.GetScrollPixelsPerUnit()
            (vx, vz) = part.GetViewStart()
            (w, h) = self.GetSize()
            if self.orientation == wx.VERTICAL:
                self.offset = vz
            elif self.orientation == wx.HORIZONTAL:
                self.offset = vx
            (p2x, p2z) = part.CalcUnscrolledPosition((vx, vz))

            if self.orientation == wx.VERTICAL:

                z = -(self.offset * unitZ % 100)
                while z < h:
                    (p3x, p3y, p3z) = part.ViewToModel((p2z, \
                        z + self.offset * unitZ))
                    label = "%d" % p3z
                    (tw, th) = dc.GetTextExtent(label)
                    if z >= clip.y-tw/2-1 and z <= clip.y+clip.height+tw/2+1:
                        dc.DrawRotatedText(label, 15-th, z + tw/2, 90)
                        dc.DrawLine(16, z, clip.width, z)
                    z += 100

            elif self.orientation == wx.HORIZONTAL:

                x = -(self.offset * unitX % 100)
                while x < w:
                    (p3x, p3y, p3z) = part.ViewToModel( \
                         (x + self.offset*unitX, p2z))
                    label = "%d" % p3x                    
                    (tw, th) = dc.GetTextExtent(label)
                    if x >= clip.x-tw/2-1 and x <= clip.x+clip.width+tw/2+1:
                        dc.DrawText(label, x-tw/2, 15-th)
                        dc.DrawLine(x, 16, x, clip.height)
                    x += 100

        finally:
            dc.SetPen(oldPen)
            dc.SetTextForeground(oldTextFg)
            dc.SetFont(oldFont)
    

    def PaintMousePointer(self, dc, clip):
        """
        Draws mouse pointer on ruler.
        """
        oldPen = dc.GetPen()
        try:
            dc.SetPen(wx.Pen('BLACK'))
            if self.orientation == wx.HORIZONTAL and self.pick != None: 
                dc.DrawLine(self.pick, 8, self.pick, 24)
            elif self.orientation == wx.VERTICAL and self.pick != None:
                dc.DrawLine(8, self.pick, 24, self.pick)
        finally:
            dc.SetPen(oldPen)


    def HandleOnScroll(self, event):
        """
        Handles scrolled window events.
        """
        if event.GetOrientation() == self.orientation:
            self.Refresh()
        event.Skip()


    def UpdateMousePointer(self, point):
        """
        Updates mouse pointers and requests repaint events.
        """
        if self.orientation == wx.HORIZONTAL:
            if self.pick == None:
                self.pick = point.x
                self.RefreshRect(wx.Rect(point.x, 0, 1, 24))
            else:
                oldPick = self.pick
                self.pick = point.x
                self.RefreshRect(wx.Rect(min(self.pick, oldPick), 0, \
                    abs(self.pick - oldPick)+1, 24))

        elif self.orientation == wx.VERTICAL:
            if self.pick == None:
                self.pick = point.y
                self.RefreshRect(wx.Rect(0, point.y, 24, 1))
            else:
                oldPick = self.pick
                self.pick = point.y
                self.RefreshRect(wx.Rect(0, min(self.pick, oldPick), 24, \
                    abs(self.pick - oldPick)+1))

        
