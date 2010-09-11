"""
Module containing main UI classes of scenery editor control.

@author adammo
"""

import math
import datetime
import logging
from decimal import Decimal

import wx
from wx.lib.evtmgr import eventManager

import model.tracks
import model.scenery
import ui.views
from sptmath import Vec3

SCALE_FACTOR = 1000.0
BASE_POINT_MARGIN = 50




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

        self.scenery = None        
        self.sceneryListener = SceneryListener(self)
        self.selection = None

        sizer.Add(corner)
        sizer.Add(self.topRuler, 0, flag = wx.EXPAND)
        sizer.Add(self.leftRuler, 0, flag = wx.EXPAND)
        sizer.Add(self.parts[0], 1, wx.EXPAND)
        sizer.AddGrowableCol(1, 1)
        sizer.AddGrowableRow(1, 1)
        
        self.SetSizer(sizer)

        self.SetBasePoint(BasePoint(Vec3(), 0.0, 0.0))


    def SetScenery(self, scenery):
        """
        Sets the scenery. Notify also active parts.
        """
        if self.scenery != None:
            self.scenery.UnregisterListener(self.sceneryListener)
        self.scenery = scenery
        self.SetSelection(None)
        self.scenery.RegisterListener(self.sceneryListener)
        for part in self.parts:
            part.SetScenery(scenery)


    def GetScenery(self):
        return self.scenery


    def SetBasePoint(self, basePoint, follow = False):
        """
        Sets the basepoint. Notify also active editor parts.
        """
        self.basePoint = basePoint
        for part in self.parts:
            part.SetBasePoint(basePoint, follow)


    def SetSelection(self, selection):
        self.selection = selection
        self.parts[0].SetSelection(selection)


    def GetSelection(self):
        return self.selection


    def CenterViewAt(self, cx, cy):
        self.parts[0].CenterViewAt(cx, cy)


    def ModelToView(self, vec3 = Vec3()):
        return self.parts[0].ModelToView(vec3)




class PlanePart(wx.ScrolledWindow):
    """
    Editor Part displaying XY view of scenery.
    """

    def __init__(self, parent, id = wx.ID_ANY):
        wx.ScrolledWindow.__init__(self, parent, id, \
            style = wx.VSCROLL | wx.HSCROLL)

        self.snapData = None
        self.basePointMover = BasePointMover(self)

        self.selectedView = None
        highlighter = Highlighter(self)

        self.wheelScaler = WheelScaler(self)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SCROLLWIN, parent.topRuler.HandleOnScroll)
        self.Bind(wx.EVT_SCROLLWIN, parent.leftRuler.HandleOnScroll)
        eventManager.Register(self.OnMoveUpdateStatusBar, wx.EVT_MOTION, self)
        eventManager.Register(self.basePointMover.OnMouseDrag, wx.EVT_MOTION, self)
        eventManager.Register(self.basePointMover.OnMousePress, wx.EVT_LEFT_DOWN, self)
        eventManager.Register(self.basePointMover.OnMouseRelease, wx.EVT_LEFT_UP, self)
        eventManager.Register(highlighter.OnMouseClick, wx.EVT_LEFT_DOWN, self)
        eventManager.Register(self.wheelScaler.OnMouseWheel, wx.EVT_MOUSEWHEEL, self)

        self.logger = logging.getLogger('Paint')

        self.scale = 1600.0
        self.GetParent().GetParent().SetStatusText("%.2f px/m" % self.scale, 2)

        self.minX = -1000.0
        self.minY = -1000.0
        self.maxX = 1000.0
        self.maxY = 1000.0

        self.extentX = 0
        self.extentY = 0

        self.trackCache = []
        self.switchCache = []
        self.basePointView = None
        
        size = self.ComputePreferredSize()
        self.SetVirtualSize(size)
        self.SetupScrolling()       
        
        
    def SetScenery(self, scenery):
        self.trackCache = []
        self.switchCache = []
        for element in scenery.RailTrackingIterator():
            self.AddView(element)
            
        self.ComputeMinMax(True)
        self.Refresh()
        
        
    def SetBasePoint(self, basePoint, follow = False):
        (vx, vy) = self.GetViewStart()
        (ux, uy) = self.GetScrollPixelsPerUnit()
        
        oldView = self.basePointView
        self.basePointView = ui.views.BasePointView(basePoint)
        if oldView != None:
            oldRect = oldView.GetRepaintBounds()
            oldRect.x -= vx * ux 
            oldRect.y -= vy * uy 
            self.RefreshRect(oldRect, False)
        needed = self.ComputeMinMax(False)        
        if needed:            
            size = self.ComputePreferredSize()
            self.SetVirtualSize(size)            
            self.Refresh()
        else:
            # Scale base point view
            self.basePointView.Scale(self.scale, self.minX, self.maxX, \
                                     self.minY, self.maxY)
            newRect = self.basePointView.GetRepaintBounds()
            newRect.x -= vx * ux
            newRect.y -= vy * uy
            self.RefreshRect(newRect, False)

        if follow:
            p = self.basePointView.point
            (wx, wy) = self.GetSize()
            if wx > 2*BASE_POINT_MARGIN and wy > 2*BASE_POINT_MARGIN:
                if p.x < vx*ux + BASE_POINT_MARGIN or p.x > vx*ux + wx - BASE_POINT_MARGIN \
                        or p.y < vy*uy + BASE_POINT_MARGIN or p.y > vy*uy + wy - BASE_POINT_MARGIN:
                    self.CenterViewAt(p.x, p.y)
            else:
                self.CenterViewAt(p.x, p.y)


    def SetSelection(self, selection):
        (vx, vy) = self.GetViewStart()
        (ux, uy) = self.GetScrollPixelsPerUnit()

        oldView = self.selectedView
        if oldView != None:
            oldRect = oldView.GetRepaintBounds()
            oldRect.x -= vx * ux
            oldRect.y -= vy * uy
            self.RefreshRect(oldRect, False)
        if selection != None:
            view = self.FindView(selection)
            if view == None:
                raise TransitionError, "Cannot find view in cache"
            self.selectedView = view
            newRect = view.GetRepaintBounds()
            newRect.x -= vx * ux
            newRect.y -= vy * uy           
            self.RefreshRect(newRect, False)            
        else:
            self.selectedView = None


    def AddView(self, element):
        view = None
        if isinstance(element, model.tracks.Track):
            view = ui.views.TrackView(element)
            self.trackCache.append(view)
        elif isinstance(element, model.tracks.Switch):
            view = ui.views.RailSwitchView(element)
            self.switchCache.append(view)
        else:
            raise ValueError("Unsupported element: " + str(type(element)))
        return view


    def FindView(self, element):
        cache = None
        if isinstance(element, model.tracks.Track):
            cache = self.trackCache
        elif isinstance(element, model.tracks.Switch):
            cache = self.switchCache
        else:
            return None

        for v in cache:
            if v.GetElement() == element:
                return v
        return None
        

    def ComputeMinMax(self, doScaling = False):
        """
        Computes bounds of scenery expressed in scenery coordinates.
        """
        nMinX = -1000.0
        nMinY = -1000.0
        nMaxX = 1000.0
        nMaxY = 1000.0

        # tracks
        for v in self.trackCache:
            (vMinX, vMaxX, vMinY, vMaxY) = v.GetMinMax()
            nMinX = min(vMinX, nMinX)
            nMaxX = max(vMaxX, nMaxX)
            nMinY = min(vMinY, nMinY)
            nMaxY = max(vMaxY, nMaxY)
        # switches
        for v in self.switchCache:
            (vMinX, vMaxX, vMinY, vMaxY) = v.GetMinMax()
            nMinX = min(vMinX, nMinX)
            nMaxX = max(vMaxX, nMaxX)
            nMinY = min(vMinY, nMinY)
            nMaxY = max(vMaxY, nMaxY)
        # base point
        (vMinX, vMaxX, vMinY, vMaxY) = self.basePointView.GetMinMax()
        nMinX = min(vMinX, nMinX)
        nMaxX = max(vMaxX, nMaxX)
        nMinY = min(vMinY, nMinY)
        nMaxY = max(vMaxY, nMaxY)

        # Changes
        if doScaling or nMinX < self.minX or nMinY < self.minY \
            or nMaxX > self.maxX or nMaxY > self.maxY:
            self.minX = min(self.minX, nMinX)
            self.minY = min(self.minY, nMinY)
            self.maxX = max(self.maxX, nMaxX)
            self.maxY = max(self.maxY, nMaxY)
            
            self.__ScaleAll(self.scale)

            return True
        else:
            return False


    def GetScale(self):
        return self.scale


    def SetScale(self, scale):
        """
        Sets the new scale, rescale all scenery elements
        and refreshes all rulers.

        Scale preserves the center view.
        """
        # 1) Get the center point of editor
        (vx, vy) = self.GetViewStart()
        (ux, uy) = self.GetScrollPixelsPerUnit()
        (sx, sy) = self.GetSize()

        p3d = self.ViewToModel((vx*ux + sx/2, vy*uy + sy/2))

        # 2) do ther right scalling
        self.scale = scale
        self.SetVirtualSize(self.ComputePreferredSize())
        self.__ScaleAll(scale)

        # 3) Move to the center of editor component
        (p2x, p2y) = self.ModelToView(p3d)
        self.CenterViewAt(p2x, p2y)

        # 4) Refresh views
        self.Update()
        self.Refresh()
        self.GetParent().topRuler.Refresh()
        self.GetParent().leftRuler.Refresh()
        self.GetParent().GetParent().SetStatusText("%.2f px/m" % scale, 2)
        
        
    def __ScaleAll(self, scale):
        for v in self.trackCache:
            v.Scale(scale, self.minX, self.maxX, self.minY, self.maxY)
        for v in self.switchCache:
            v.Scale(scale, self.minX, self.maxX, self.minY, self.maxY)
        self.basePointView.Scale(scale, self.minX, self.maxX, self.minY, \
                                 self.maxY)


    def ViewToModel(self, point):
        """
        Converts 2D point of UI editor coordinates into 3D point
        of scenery coordinates.
        """
        p3d = Vec3(Decimal(str((point[0]-100)/self.scale * SCALE_FACTOR + self.minX)), \
            Decimal(str(-((point[1]-100)/self.scale * SCALE_FACTOR - self.maxY))), \
            Decimal(0))
        return p3d


    def ModelToView(self, point = Vec3()):
        """
        Converts 3D point of scenery coordiante into 2D point of
        UI editor coordinates.
        """        
        p2d = (int((float(point.x) - self.minX) * self.scale / SCALE_FACTOR + 100), \
            int((-float(point.y) + self.maxY) * self.scale / SCALE_FACTOR + 100))
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
        self.Layout()


    def ComputePreferredSize(self):
        (w, h) = self.GetSize()
        
        return (max(w, int(self.scale * (self.maxX - self.minX) \
                / SCALE_FACTOR) + 200) + self.extentX,
            max(h + self.extentY, int(self.scale * (self.maxY - self.minY) \
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
        center2D = self.ModelToView(Vec3())

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
        y = int((self.maxY - self.minY) * self.scale / SCALE_FACTOR) + 100

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
        self.PaintSelection(dc, clip)
        self.PaintSnapPoint(dc, clip)
        self.PaintBasePoint(dc, clip)
        
        
    def PaintTracks(self, dc, clip):
        """
        Paint rail tracks.
        """        
        oldPen = dc.GetPen()
        try:
            dc.SetPen(wx.Pen((34, 139, 34), \
                3 if self.scale >= 1000.0 else 1))
            for v in self.trackCache:
                if v != self.selectedView:
                    v.Draw(dc, clip)
        finally:
            dc.SetPen(oldPen)
            
            
    def PaintSwitches(self, dc, clip):
        """
        Paints rail switches.
        """
        oldPen = dc.GetPen()
        try:
            dc.SetPen(wx.Pen((173, 255, 47), \
                3 if self.scale >= 1000.0 else 1))
            for v in self.switchCache:
                if v != self.selectedView:
                    v.Draw(dc, clip)
        finally:
            dc.SetPen(oldPen)


    def PaintSelection(self, dc, clip):
        """
        Paints rail switches.
        """
        if self.selectedView == None:
            return
        oldPen = dc.GetPen()
        try:
            dc.SetPen(wx.Pen((255, 0, 0), \
                3 if self.scale >= 1000.0 else 1))
            self.selectedView.Draw(dc, clip)
        finally:
            dc.SetPen(oldPen)
            
            
    def PaintBasePoint(self, dc, clip):
        self.basePointView.Draw(dc, clip)


    def PaintSnapPoint(self, dc, clip):
        if self.snapData != None:
             index = ui.views.getImageIndexByAngle(self.snapData.alpha)

             dc.DrawBitmap(wx.BitmapFromImage(ui.views.SNAP_BASEPOINT_IMAGES[index]), \
                 self.snapData.p2d.x - ui.views.SNAP_BASEPOINT_IMAGES[index].GetWidth()/2, \
                 self.snapData.p2d.y - ui.views.SNAP_BASEPOINT_IMAGES[index].GetHeight()/2)


    def OnMoveUpdateStatusBar(self, event):
        """
        Updates 3D coordinates in case of mouse movement on frame status bar.
        """
        opoint = event.GetPosition()
        point = self.CalcUnscrolledPosition(event.GetPosition())
        p3d = self.ViewToModel(point)

        bar = self.GetParent().GetParent().GetStatusBar()
        bar.SetStatusText("%.3f, %.3f, %.3f" % (p3d.x, p3d.y, p3d.z), 1)

        self.GetParent().topRuler.UpdateMousePointer(opoint)
        self.GetParent().leftRuler.UpdateMousePointer(opoint)


    def SetSize(self, size):
        print size
        wx.Panel.SetSize(size)




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
            (unitX, unitY) = part.GetScrollPixelsPerUnit()
            # Here is a problem with GetViewStart method under wxGTK
            (vx, vy) = part.GetViewStart()
            (w, h) = self.GetSize()
            if self.orientation == wx.VERTICAL:
                self.offset = vy
            elif self.orientation == wx.HORIZONTAL:
                self.offset = vx
            (p2x, p2y) = part.CalcUnscrolledPosition((vx, vy))

            if self.orientation == wx.VERTICAL:

                y = -(self.offset * unitY % 100)
                while y < h:
                    p3d = part.ViewToModel((p2x, \
                        y + self.offset * unitY))
                    label = "%d" % p3d.y
                    (tw, th) = dc.GetTextExtent(label)
                    if y >= clip.y-tw/2-1 and y <= clip.y+clip.height+tw/2+1:
                        dc.DrawRotatedText(label, 15-th, y + tw/2, 90)
                        dc.DrawLine(16, y, clip.width, y)
                    y += 100

            elif self.orientation == wx.HORIZONTAL:

                x = -(self.offset * unitX % 100)
                while x < w:
                    p3d = part.ViewToModel( \
                         (x + self.offset*unitX, p2y))
                    label = "%d" % p3d.x
                    (tw, th) = dc.GetTextExtent(label)
                    if x >= clip.x-tw/2-1 and x <= clip.x+clip.width+tw/2+1:
                        dc.DrawText(label, x - tw/2, 15 - th)
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

        


class BasePoint:
    """
    Base point.
    Defines a vector attached in some 3D world point that allows
    additions to the scenery.

    Gradient is expressed in pro milles.
    """
    
    def __init__(self, p=Vec3(), alpha = 0, gradient = 0):
        self.point = p
        self.alpha = alpha
        self.gradient = gradient
        
    
    def __repr__(self):
        return u"BasePoint[point=(%.3f, %.3f, %.3f),alpha=%.2f,gradient=%.2f\u2030]" % \
           (self.point.x, self.point.y, self.point.z, \
            self.alpha, self.gradient)
    
    
    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, BasePoint):
            return False
        return self.point == other.point and self.alpha == other.alpha and \
            self.gradient == other.gradient




class BasePointMover:
    """
    Helper class that moves a basepoint respectively to the mouse drags.
    """
    
    def __init__(self, editorPart):
        self.editorPart = editorPart
        self.enabled = True
        self.pressed = False
        
        
    def OnMousePress(self, event):
        if not self.enabled:
            return
        
        point = self.editorPart.CalcUnscrolledPosition(event.GetPosition())
        
        if self.editorPart.basePointView.IsSelectionPossible(point):
            self.pressed = True
    
    
    def OnMouseRelease(self, event):
        if not self.enabled:
            return
       
        snapData = self.editorPart.snapData 
        point = self.editorPart.CalcUnscrolledPosition(event.GetPosition())
        
        if self.pressed:
            if snapData != None:
                self.editorPart.GetParent().basePoint.point = snapData.p3d
                self.editorPart.GetParent().basePoint.alpha = snapData.alpha
                self.editorPart.GetParent().basePoint.gradient = snapData.gradient
            else:
                p3d = self.editorPart.ViewToModel(point)
                self.editorPart.GetParent().basePoint.point = p3d
            self.editorPart.GetParent().SetBasePoint( \
                self.editorPart.GetParent().basePoint)
            
        self.pressed = False
        self.editorPart.snapData = None
    
    
    def OnMouseDrag(self, event):
        if self.pressed:
            oldSnapData = self.editorPart.snapData 
            point = self.editorPart.CalcUnscrolledPosition(event.GetPosition())

            foundSnapData = None
           
            for v in self.editorPart.trackCache + self.editorPart.switchCache:
                foundSnapData = v.GetSnapData(point)
                if foundSnapData != None:
                    self.editorPart.snapData = foundSnapData
                    break
 
            if foundSnapData == None:
                self.editorPart.snapData = None
            if oldSnapData != None:
                self.editorPart.RefreshRect( \
                    wx.Rect(oldSnapData.p2d.x-10, oldSnapData.p2d.y-10, 20, 20), \
                    False)
            if foundSnapData != None:
                self.editorPart.RefreshRect( \
                    wx.Rect(foundSnapData.p2d.x-10, foundSnapData.p2d.y-10, 20, 20), \
                    False)




class SnapData:
    """
    Data object containing snap information.
    """
    
    def __init__(self):
        self.alpha = 0.0
        self.gradient = 0.0
        self.p2d = (0, 0)
        self.p3d = Vec3()
        
    
    def __repr__(self):
        return u"SnapData[p2d=(%d,%d),p3d=%s,alpha=%.2f,gradient=%.2f\u2030]" \
            % (self.p2d[0], self.p2d[1], self.p3d, self.alpha, self.gradient)


    def Complete(self, railTracking):
        v = railTracking.getNormalVector(self.p3d)
        x, y, z = float(v.x), float(v.y), float(v.z)
        self.alpha = math.degrees(math.atan2(x, y))
        self.gradient = 1000.0*z / math.sqrt(x*x + y*y)




class Highlighter:
    """
    Mouse listener that make selection in editor
    """

    def __init__(self, editorPart):
        self.editorPart = editorPart


    def OnMouseClick(self, event):
        if not self.editorPart.basePointMover.pressed:
            point = self.editorPart.CalcUnscrolledPosition(event.GetPosition())

            startTime = datetime.datetime.now()
            try:
                found = None
                for v in self.editorPart.trackCache + self.editorPart.switchCache:
                    if v.IsSelectionPossible(point):
                        found = v
                        break
                if found != None:
                    self.editorPart.GetParent().SetSelection(found.GetElement())
            finally:
                delta = datetime.datetime.now() - startTime
                idelta = delta.days * 86400 + delta.seconds * 1000000 \
                    + delta.microseconds
                self.editorPart.logger.debug(u"Selection lasted %d \u00b5s" % idelta)




class WheelScaler:
    """
    Responds to mouse wheel in scenery editor and adjust the scale.
    """

    def __init__(self, editor):
        self.editor = editor


    def OnMouseWheel(self, event):
        if event.ControlDown():
            delta = event.GetWheelRotation()
            scale = self.editor.GetScale()
            if delta < 0:
                self.editor.SetScale(scale * 2)
            else:
                self.editor.SetScale(scale / 2)
        else:
            event.Skip()




class SceneryListener(model.scenery.SceneryListener):
    """
    Responds to the changs in scenery
    """

    def __init__(self, editor):
        model.scenery.SceneryListener.__init__(self)
        self.editor = editor


    def sceneryChanged(self, event):
        element = event.GetElement()
        changeType = event.GetType()

        part = self.editor.parts[0]
        (vx, vy) = part.GetViewStart()
        (ux, uy) = part.GetScrollPixelsPerUnit()

        view = None
        if changeType == model.scenery.CHANGE_ADD:
            view = part.AddView(element)
        elif changeType == model.scenery.CHANGE_REMOVE:
            if element == self.editor.GetSelection():
                 self.editor.SetSelection(None)
            view = part.FindView(element)
            part.trackCache.remove(view)

        needPainting = part.ComputeMinMax()
        if needPainting:
            self.editor.Refresh()
        else:
            if changeType == model.scenery.CHANGE_ADD:
                view.Scale(part.scale, part.minX, part.maxX, part.minY, part.maxY)
        
            repaintRect = view.GetRepaintBounds()
            repaintRect.x -= vx * ux
            repaintRect.y -= vy * uy
            part.RefreshRect(repaintRect, False)
      

