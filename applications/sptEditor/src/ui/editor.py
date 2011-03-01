"""
Module containing main UI classes of scenery editor control.

@author adammo
"""

import math
import datetime
import logging
from sptmath import Decimal

import wx
from wx.lib.evtmgr import eventManager

import Application
import model.tracks
import model.scenery
import ui.views
import ui.trackfc
from sptmath import Vec3


# Constants here
SCALE_MIN = 0.004 # It gives 800px/200km
SCALE_MAX = 2000.0 # It gives 2000px/m
SCALE_DEFAULT = 1.0 # It gives 1px/m
BASE_POINT_MARGIN = 50

# Modes of editor
MODE_NORMAL = 0 # default
MODE_CLOSURE = 1 # closure track mode




class SceneryEditor(wx.Panel):
    """
    Scenery editor control.
    """

    def __init__(self, parent, main_window, id = wx.ID_ANY):
        wx.Panel.__init__(self, parent, id, style = wx.BORDER_SUNKEN)
        
        sizer = wx.FlexGridSizer(2, 2, 1, 1)

        corner = wx.Panel(self, name = "Corner")
        corner.SetBackgroundColour('WHITE')
        self.leftRuler = Ruler(self, orientation = wx.VERTICAL, \
            name = "Left ruler")
        self.topRuler = Ruler(self, orientation = wx.HORIZONTAL, \
            name = "Top ruler")
        self.parts = [PlanePart(self, main_window)]

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


    def CenterViewAt(self, x, y):
        self.parts[0].CenterViewAt((x,y))


    def ModelToView(self, vec3 = Vec3()):
        return self.parts[0].ModelToView(vec3)


    def SetMode(self, mode):
        self.parts[0].SetMode(mode)

    def OnMouseWheel(self, event):
        self.parts[0].OnMouseWheel(event)
        #TODO
        #For for all array self.parts


class PlanePart(wx.ScrolledWindow):
    """
    Editor Part displaying XY view of scenery.
    """

    def __init__(self, parent, main_window, id = wx.ID_ANY):
        wx.ScrolledWindow.__init__(self, parent, id, \
            style = wx.VSCROLL | wx.HSCROLL)

        self.main_window = main_window
        self.snapData = None
        self.basePointMover = BasePointMover(self)

        self.selectedView = None
        self.highlighter = Highlighter(self)

        self.wheelScaler = WheelScaler(self)        
        self.sceneryDragger = SceneryDragger(self)
        self.trackClosurer = TrackClosurer(self)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.mouse_in_window = False
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Bind(wx.EVT_SCROLLWIN, parent.topRuler.HandleOnScroll)
        self.Bind(wx.EVT_SCROLLWIN, parent.leftRuler.HandleOnScroll)
        
        eventManager.Register(self.OnMoveUpdateStatusBar, wx.EVT_MOTION, self)
        eventManager.Register(self.basePointMover.OnMouseDrag, wx.EVT_MOTION, self)
        eventManager.Register(self.basePointMover.OnMousePress, wx.EVT_LEFT_DOWN, self)
        eventManager.Register(self.basePointMover.OnMouseRelease, wx.EVT_LEFT_UP, self)
        eventManager.Register(self.highlighter.OnMouseClick, wx.EVT_LEFT_DOWN, self)
        eventManager.Register(self.wheelScaler.OnMouseMove, wx.EVT_MOTION, self)
        eventManager.Register(self.sceneryDragger.OnMousePress, wx.EVT_MIDDLE_DOWN, self)
        eventManager.Register(self.sceneryDragger.MoveScenery, wx.EVT_MOTION, self)
        eventManager.Register(self.trackClosurer.OnMouseClick, wx.EVT_LEFT_UP, self)

        self.logger = logging.getLogger('Paint')

        self.scale = SCALE_DEFAULT
        self.main_window.SetStatusText("%.3f px/m" % self.scale, 2)

        self.minX = -1000.0
        self.minY = -1000.0
        self.maxX = 1000.0
        self.maxY = 1000.0

        self.extentX = 0
        self.extentY = 0

        self.trackCache = []
        self.switchCache = []
        self.basePointView = None

        self.mode = MODE_NORMAL
        
        size = self.ComputePreferredSize()
        self.SetVirtualSize(size)
        self.SetupScrolling()       
        #self.SetFocusIgnoringChildren()

    def OnMouseEnter(self, event):
        self.mouse_in_window = True

    def OnMouseLeave(self, event):
        self.mouse_in_window = False

    def OnMouseWheel(self, event):
        #print "Editor mouse event"
        if self.mouse_in_window:
            self.wheelScaler.OnMouseWheel(event)

    def SetScenery(self, scenery):
        self.trackCache = []
        self.switchCache = []
        for e in scenery.tracks.tracks():
            self.AddView(e)
        for e in scenery.tracks.switches():
            self.AddView(e)
            
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
            self.RefreshRect(oldRect)
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
            self.RefreshRect(newRect)

        if follow:
            p = self.basePointView.point
            (wx, wy) = self.GetSize()
            if wx > 2*BASE_POINT_MARGIN and wy > 2*BASE_POINT_MARGIN:
                if p.x < vx*ux + BASE_POINT_MARGIN or p.x > vx*ux + wx - BASE_POINT_MARGIN \
                        or p.y < vy*uy + BASE_POINT_MARGIN or p.y > vy*uy + wy - BASE_POINT_MARGIN:
                    self.CenterViewAt(p.x, p.y)
            else:
                self.CenterViewAt(p.x, p.y)


    def SetMode(self, mode, updateMenu = False):
        self.__mode = mode
        if mode == MODE_NORMAL:
            self.trackClosurer.SetEnabled(False)
            self.highlighter.SetEnabled(True)
            if updateMenu:
                # Find menu item 
                mainWindow = wx.FindWindowById(Application.ID_MAIN_FRAME)
                mainMenu = mainWindow.GetMenuBar()
                miTrackNormal = mainMenu.FindItemById(wx.xrc.XRCID('ID_MODE_TRACK_NORMAL'))
                miTrackNormal.Check()
        elif mode == MODE_CLOSURE:
            self.trackClosurer.SetEnabled(True)
            self.highlighter.SetEnabled(False)


    def SetSelection(self, selection):
        (vx, vy) = self.GetViewStart()
        (ux, uy) = self.GetScrollPixelsPerUnit()

        oldView = self.selectedView
        if oldView != None:
            oldRect = oldView.GetRepaintBounds()
            oldRect.x -= vx * ux
            oldRect.y -= vy * uy
            self.RefreshRect(oldRect)
        if selection != None:
            view = self.FindView(selection)
            if view == None:
                raise TransitionError, "Cannot find view in cache"
            self.selectedView = view
            newRect = view.GetRepaintBounds()
            newRect.x -= vx * ux
            newRect.y -= vy * uy           
            self.RefreshRect(newRect)            
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

    def CalculateCenterPointOfEditor(self):
         # 1) Get the center point of editor
        (view_start_x, view_start_y) = self.GetViewStart()
        (window_size_width, window_size_height) = self.GetSize()
        (scroll_rate_x, scroll_rate_y) = self.GetScrollPixelsPerUnit()
        
        #return position we calc (position of center of the screen)
        return wx.Point(view_start_x*scroll_rate_x + window_size_width / 2, \
                view_start_y * scroll_rate_y + window_size_height / 2)
        
    def GetScale(self):
        return self.scale


    def SetScale(self, scale, position=None):
        """
        Sets the new scale, rescale all scenery elements
        and refreshes all rulers.

        Scale preserves the center view.
        """
        # Set limits to the scale
        if scale > SCALE_MAX + 0.001 or scale < SCALE_MIN - 0.001:
            return

        # 1) Get the center point of editor
        #if it's not position we calc position of center of the screen
        if position == None:
            position = self.CalculateCenterPointOfEditor()
        
        #recalculate point to model (in mm) because we cannot scale point directly
        p3d = self.ViewToModel(position)
        print "Center to point:"
        print p3d
        # 2) do scalling
        self.scale = scale
        self.SetVirtualSize(self.ComputePreferredSize())
        self.__ScaleAll(scale)

        # 3) Move to the center of editor component
        new_position = self.ModelToView(p3d)
        self.CenterViewAt(new_position)

        # 4) Refresh views
        self.Update()
        self.Refresh()
        #self.GetParent().topRuler.Refresh()
        #self.GetParent().leftRuler.Refresh()
        self.main_window.SetStatusText("%.3f px/m" % scale, 2)
        
        
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
        p3d = Vec3(Decimal(str((point[0]-100)/self.scale + self.minX)), \
            Decimal(str(-((point[1]-100)/self.scale - self.maxY))), \
            Decimal())
        return p3d


    def ModelToView(self, point = Vec3()):
        """
        Converts 3D point of scenery coordiante into 2D point of
        UI editor coordinates.
        """        
        p2d = (int((float(point.x) - self.minX) * self.scale + 100), \
            int((-float(point.y) + self.maxY) * self.scale + 100))
        return p2d

    def CenterViewAt(self, requiered_position = wx.Point()):
        self.CenterViewAt((requiered_position.x, requiered_position.y))

    def CenterViewAt(self, (requiered_position_x, requiered_position_y)):
        """
        Centers the view on following point in pixels.
        """
        #gaterring necessary information
        (window_size_width, window_size_height) = self.GetSize()
        (scroll_rate_x, scroll_rate_y) = self.GetScrollPixelsPerUnit()
        
        #calculate position of left upper corner to which we scroll
        corner_x = max(0,requiered_position_x - (window_size_width / 2))
        corner_y = max(0, requiered_position_y - (window_size_height / 2))
        
        #scroll to reqiered position
        self.Scroll(corner_x / scroll_rate_x, corner_y / scroll_rate_y)
        #refresh rulers
        self.GetParent().leftRuler.Refresh()
        self.GetParent().topRuler.Refresh()

    def OnSize(self, event):
        self.Refresh()
        self.GetParent().leftRuler.Refresh()
        self.GetParent().topRuler.Refresh()
        self.Layout()


    def ComputePreferredSize(self):
        (w, h) = self.GetSize()
        
        return (max(w, int(self.scale * (self.maxX - self.minX)) \
                + 200) + self.extentX,
            max(h + self.extentY, int(self.scale * (self.maxY - self.minY)) \
               + 200) + self.extentY)


    def SetupScrolling(self):
        """
        Sets up scrolling of the window.
        """
        self.SetScrollRate(1, 1)


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
        x = int((self.maxX - self.minX) * self.scale) + 100
        y = int((self.maxY - self.minY) * self.scale) + 100

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
                3 if self.scale > 1.0 else 1))
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
                3 if self.scale > 1.0 else 1))
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
                3 if self.scale > 1.0 else 1))
            self.selectedView.Draw(dc, clip)
        finally:
            dc.SetPen(oldPen)
            
            
    def PaintBasePoint(self, dc, clip):
        self.basePointView.Draw(dc, clip)


    def PaintSnapPoint(self, dc, clip):
        if self.snapData != None:
             index = ui.views.getImageIndexByAngle(self.snapData.alpha)
             snapImage = ui.views.SNAP_BASEPOINT_IMAGES[index]

             dc.DrawBitmap(wx.BitmapFromImage(snapImage), \
                 self.snapData.p2d.x - snapImage.GetWidth()/2, \
                 self.snapData.p2d.y - snapImage.GetHeight()/2)


    def OnMoveUpdateStatusBar(self, event):
        """
        Updates 3D coordinates in case of mouse movement on frame status bar.
        """
        opoint = event.GetPosition()
        point = self.CalcUnscrolledPosition(event.GetPosition())
        p3d = self.ViewToModel(point)
        #bar = self.GetParent().GetParent().GetStatusBar()
        self.main_window.SetStatusText("%.3f, %.3f, %.3f" % (p3d.x, p3d.y, p3d.z), 1)

        self.GetParent().topRuler.UpdateMousePointer(opoint)
        self.GetParent().leftRuler.UpdateMousePointer(opoint)


    def SetSize(self, size):
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
                    label = "%.2f" % p3d.y
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
                    label = "%.2f" % p3d.x
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
            updateScreen = False
            
            # This may be optimised by using scenery outline points
            for v in self.editorPart.trackCache + self.editorPart.switchCache:
                foundSnapData = v.GetSnapData(point)
                if foundSnapData != None:
                    self.editorPart.snapData = foundSnapData
                    break
 
            if foundSnapData == None:
                self.editorPart.snapData = None
            if oldSnapData != None:
                self.editorPart.RefreshRect( \
                    wx.Rect(oldSnapData.p2d.x-10, oldSnapData.p2d.y-10, 20, 20))
                updateScreen = True
            if foundSnapData != None:
                self.editorPart.RefreshRect( \
                    wx.Rect(foundSnapData.p2d.x-10, foundSnapData.p2d.y-10, 20, 20))
                updateScreen = True
            if updateScreen:
                self.editorPart.Update()




class SceneryDragger:
    """
    Dragger of scenery. This handles mouse drag with middle button pressed
    modifier for move scenery.
    """

    def __init__(self, editor):
        self.editor = editor
        self.dragStart = None


    def OnMousePress(self, event):
        """
        Gets the initial position of dragging.
        """
        if event.MiddleDown():
            self.dragStart = event.GetPosition()

    def MoveScenery(self, event):
        """
        Move scenery by move of mouse.
        """
        #check if button is pressed
        if event.MiddleIsDown():
            #calculate move of mouse, center of screen and scroll to new position
            delta = event.GetPosition() - self.dragStart
            center_point = self.editor.CalculateCenterPointOfEditor()
            self.editor.CenterViewAt(center_point - delta)
            
            #remember of position of mouse
            self.dragStart = event.GetPosition()
            
            #refresh rulers
            self.editor.GetParent().leftRuler.Refresh()
            self.editor.GetParent().topRuler.Refresh()


class TrackClosurer:
    """
    Closure track mouse listener handles creating track closure
    if editor mode is MODE_CLOSURE
    """

    def __init__(self, editor):
        self.__editor = editor
        # This listener may be switched on or off
        self.__enabled = False
        self.__startPoint = None
        self.__startElement = None


    def SetEnabled(self, enabled = True):
        self.__enabled = enabled
        if not enabled:
            self.__startPoint = None
            self.__startElement = None


    def OnMouseClick(self, event):
        if not self.__enabled:
            return # Return immediately

        point = self.__editor.CalcUnscrolledPosition(event.GetPosition())

        startTime = datetime.datetime.now()
        try:
            foundView = None
            for v in self.__editor.trackCache + self.__editor.switchCache:
                if v.IsSelectionPossible(point):
                    foundView = v
                    break
            if foundView is None:
                # Reset mode to default
                self.__editor.SetMode(MODE_NORMAL)
            else:
                snapData = foundView.GetSnapData(point)
                snapElement = foundView.GetElement()

                if self.__startPoint is not None:
                    # Handle second point by creating closure track and adding it to scenery
                    _trackfc = ui.trackfc.TrackFactory(self.__editor)
                    closureTrack = _trackfc.CreateClosureTrack( \
                        self.__startElement, self.__startPoint, snapElement, snapData.p3d)
                    scenery = self.__editor.GetParent().GetScenery()
                    scenery.AddRailTracking(closureTrack)

                    # Reset editor mode
                    self.__editor.SetMode(MODE_NORMAL, True)
                else:
                    # Handle first point (store it only)
                    self.__startPoint = snapData.p3d
                    self.__startElement = snapElement
        finally:
            delta = datetime.datetime.now() - startTime
            idelta = delta.days * 86400 + delta.seconds * 1000000 \
                + delta.microseconds
            self.__editor.logger.debug(u"Create closure track lasted %d \u00b5s" % idelta)




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
        self.__enabled = True


    def SetEnabled(self, enabled = True):
        self.__enabled = enabled


    def OnMouseClick(self, event):
        if self.__enabled and not self.editorPart.basePointMover.pressed:
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

    def OnMouseMove(self, event):
        self.mouse_position = event.GetPosition()
        
    def OnMouseWheel(self, event):
        print "Mouse wheel event"
        #print "Wheel rotation:"
        #print event.GetWheelRotation()
        delta = event.GetWheelRotation()
        #Logical position of mouse is retrieved in unscrolled values
        mouse_logical_position_in_window = self.editor.CalcUnscrolledPosition(self.mouse_position)
                
        scale = self.editor.GetScale()
        if delta < 0:
            self.editor.SetScale(scale / 2, mouse_logical_position_in_window)
        else:
            self.editor.SetScale(scale * 2, mouse_logical_position_in_window)



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

        if changeType == model.scenery.CHANGE_ADD \
            and isinstance(element, model.groups.RailContainer):

            self.sceneryAddGroup(element)
        elif changeType == model.scenery.CHANGE_ADD:
            self.sceneryAdd(element)
        elif changeType == model.scenery.CHANGE_REMOVE:
            self.sceneryRemove(element)
      

    def sceneryAdd(self, element):
        part = self.editor.parts[0]
        (vx, vy) = part.GetViewStart()
        (ux, uy) = part.GetScrollPixelsPerUnit()

        view = part.AddView(element)

        needPainting = part.ComputeMinMax()
        if needPainting:
            self.editor.Refresh()
        else:
            view.Scale(part.scale, part.minX, part.maxX, part.minY, part.maxY)
        
            repaintRect = view.GetRepaintBounds()
            repaintRect.x -= vx * ux
            repaintRect.y -= vy * uy
            part.RefreshRect(repaintRect)
    

    def sceneryRemove(self, element):
        part = self.editor.parts[0]
        (vx, vy) = part.GetViewStart()
        (ux, uy) = part.GetScrollPixelsPerUnit()

        if element == self.editor.GetSelection():
            self.editor.SetSelection(None)
        view = part.FindView(element)
        if type(element) is model.tracks.Track:
            part.trackCache.remove(view)
        elif type(element) is model.tracks.Switch:
            part.switchCache.remove(view)

        needPainting = part.ComputeMinMax()
        if needPainting:
            self.editor.Refresh()
        else:
            repaintRect = view.GetRepaintBounds()
            repaintRect.x -= vx * ux
            repaintRect.y -= vy * uy
            part.RefreshRect(repaintRect)


    def sceneryAddGroup(self, group):
        part = self.editor.parts[0]
        (vx, vy) = part.GetViewStart()
        (ux, uy) = part.GetScrollPixelsPerUnit()

        views = []
        for track in group.tracks():
            views.append(part.AddView(track))
        for sw in group.switches():
            views.append(part.AddView(sw))

        needPainting = part.ComputeMinMax()
        if needPainting:
            self.editor.Refresh()
        else:
            repaintRect = None
            for view in views:
                view.Scale(part.scale, part.minX, part.maxX, part.minY, part.maxY)
                nextRepaintRect = view.GetRepaintBounds()
                if repaintRect is None:
                    repaintRect = nextRepaintRect
                else:
                    repaintRect = repaintRect.Union(nextRepaintRect)

            repaintRect.x -= vx * ux
            repaintRect.y -= vy * uy
            part.RefreshRect(repaintRect)

