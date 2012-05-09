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

#import Application
import sptial
import model.tracks
import model.scenery
from ui.rulers import Ruler
import ui.views
import ui.trackfc
from sptmath import Vec3
import copy

# Constants here
SCALE_MIN = 0.004 # It gives 800px/200km
SCALE_MAX = 2000.0 # It gives 2000px/m
SCALE_DEFAULT = 1.0 # It gives 1px/m
BASE_POINT_MARGIN = 50
MANUAL_SCROLL_RATE_X = 30
MANUAL_SCROLL_RATE_Y = 30


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
        self.leftRuler = Ruler(self, orientation = wx.VERTICAL,
            name = "Left ruler")
        self.topRuler = Ruler(self, orientation = wx.HORIZONTAL,
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
        if self.scenery is not None:
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

        #load properties of selected object
        self.TopLevelParent.propertiesPaletteFrame.LoadToolPropertiesByType(selection)
        

    def GetSelection(self):
        return self.selection


    def CenterViewAt(self, x, y):
        self.parts[0].CenterViewAt((x,y))


    def ModelToView(self, vec3 = Vec3()):
        return self.parts[0].ModelToView(vec3)


    def SetMode(self, mode, updateMenu = False):
        self.parts[0].SetMode(mode)
        #update menu
        if updateMenu != False:
            self.GetTopLevelParent().MenuChangeEditorMode(mode)
            
    def OnMouseWheel(self, event):
        self.parts[0].OnMouseWheel(event)
        #TODO
        #For for all array self.parts


class PlanePart(wx.ScrolledWindow):
    """
    Editor Part displaying XY view of scenery.
    """

    def __init__(self, parent, main_window, id = wx.ID_ANY):
        wx.ScrolledWindow.__init__(self, parent, id,
            style = wx.VSCROLL | wx.HSCROLL)

        self.main_window = main_window
        self.snapData = None
        self.basePointMover = BasePointMover(self)

        self.selected = None
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
        self.Bind(wx.EVT_SCROLLWIN_LINEUP, self.OnScrollUp)
        self.Bind(wx.EVT_SCROLLWIN_LINEDOWN, self.OnScrollDown)

        eventManager.Register(self.OnMoveUpdateStatusBar, wx.EVT_MOTION, self)
        eventManager.Register(self.basePointMover.OnMouseDrag, wx.EVT_MOTION, self)
        eventManager.Register(self.basePointMover.OnMousePress, wx.EVT_LEFT_DOWN, self)
        eventManager.Register(self.basePointMover.OnMouseRelease, wx.EVT_LEFT_UP, self)
        eventManager.Register(self.highlighter.OnMouseClick, wx.EVT_LEFT_DOWN, self)
        #eventManager.Register(self.highlighter.OnMouseMove, wx.EVT_MOTION, self)
        eventManager.Register(self.wheelScaler.OnMouseMove, wx.EVT_MOTION, self)
        eventManager.Register(self.sceneryDragger.OnMousePress, wx.EVT_MIDDLE_DOWN, self)
        eventManager.Register(self.sceneryDragger.MoveScenery, wx.EVT_MOTION, self)
        eventManager.Register(self.trackClosurer.OnMouseClick, wx.EVT_LEFT_UP, self)

        self.logger = logging.getLogger('Paint')

        self.main_window.SetStatusText("%.3f px/m" % SCALE_DEFAULT, 2)

        self.bounds = EditorBounds()

        self.basePointView = None

        self._pen_rail_tracking_width = 1

        self.mode = MODE_NORMAL
        
        self.Resize()
        self.SetupScrolling()       
        #self.SetFocusIgnoringChildren()

    def OnScrollUp(self, event):
        '''
        Change scroll rate for scroll buttons use
        '''
        
        cp = self.CalculateCenterPointOfEditor()
        if (event.GetOrientation() == wx.HORIZONTAL):
            cp.x -= MANUAL_SCROLL_RATE_X
        else:
            cp.y -= MANUAL_SCROLL_RATE_Y
        self.CenterViewAt((cp.x, cp.y))
    
    def OnScrollDown(self, event):
        '''
        Change scroll rate for scroll buttons use
        '''
        cp = self.CalculateCenterPointOfEditor()
        if (event.GetOrientation() == wx.HORIZONTAL):
            cp.x += MANUAL_SCROLL_RATE_X
        else:
            cp.y += MANUAL_SCROLL_RATE_Y
        self.CenterViewAt((cp.x, cp.y))
        
    def OnMouseEnter(self, event):
        #Inform window that mouse is in area. Set focus to the ribbon
        #to correct assign mouse wheel events.
        self.mouse_in_window = True
        self.main_window._menubar.SetFocus()
        #self.logger.info("Mouse enter the window")
        #print "mouse enter"

    def OnMouseLeave(self, event):
        #inform window that mouse is out of the area.
        self.mouse_in_window = False
        #self.logger.info("Mouse leave the window")
        #print "mouse leave"

    def OnMouseWheel(self, event):
        #print "Editor mouse event"
        if self.mouse_in_window:
            self.wheelScaler.OnMouseWheel(event)

    def SetScenery(self, scenery):
        mbc = scenery.GetMbc()
        self.bounds.Update(mbc.min(), mbc.max())
        self.Refresh()
        
        
    def GetScenery(self):
        return self.GetParent().GetScenery()
        
        
    def SetBasePoint(self, basePoint, follow = False):
        (vx, vy) = self.GetViewStart()
        (ux, uy) = self.GetScrollPixelsPerUnit()

        oldView = self.basePointView
        self.basePointView = ui.views.BasePointView(basePoint)
        if oldView is not None:
            oldRect = oldView.GetBox(self.bounds)
            self.RedrawRect(oldRect)
        needed = self.bounds.Update(basePoint.point)
        if needed:
            self.Resize()
        else:
            rect = self.basePointView.GetBox(self.bounds)
            self.RedrawRect(rect)
        
        if follow:
            p = self.bounds.ModelToView(basePoint.point)
            (wx, wy) = self.GetSize()
            if wx > 2*BASE_POINT_MARGIN and wy > 2*BASE_POINT_MARGIN:
                if (p[0] < vx*ux + BASE_POINT_MARGIN or p[0] > vx*ux + wx - BASE_POINT_MARGIN
                        or p[1] < vy*uy + BASE_POINT_MARGIN or p[1] > vy*uy + wy - BASE_POINT_MARGIN):
                    self.CenterViewAt(p)
            else:
                self.CenterViewAt(p)


    def SetMode(self, mode, updateMenu = False):
        self.__mode = mode
        if mode == MODE_NORMAL:
            self.trackClosurer.SetEnabled(False)
            self.highlighter.SetEnabled(True)
        elif mode == MODE_CLOSURE:
            self.trackClosurer.SetEnabled(True)
            self.highlighter.SetEnabled(False)
        if updateMenu:
            self.GetTopLevelParent().MenuChangeEditorMode(mode)


    def SetSelection(self, selection):
        #(vx, vy) = self.GetViewStart()
        #(ux, uy) = self.GetScrollPixelsPerUnit()

        oldView = self.selected
        if (oldView is not None):
            tv = ui.views.GetViewer(oldView)
            self.RedrawRect(tv.GetBox(self.bounds))
        
        self.selected = selection
        if (selection is not None):
            tv = ui.views.GetViewer(selection)
            self.RedrawRect(tv.GetBox(self.bounds))
            
    def CalculateCenterPointOfEditor(self):
        # 1) Get the center point of editor
        (view_start_x, view_start_y) = self.GetViewStart()
        (window_size_width, window_size_height) = self.GetSize()
        (scroll_rate_x, scroll_rate_y) = self.GetScrollPixelsPerUnit()
        
        #return position we calc (position of center of the screen)
        return wx.Point(view_start_x*scroll_rate_x + window_size_width / 2, \
                view_start_y * scroll_rate_y + window_size_height / 2)
        
    def GetScale(self):
        return self.bounds.scale


    def SetScale(self, scale, position=None):
        """
        Sets the new scale, rescale all scenery elements
        and refreshes all rulers.

        Scale preserves the center view.
        """
        assert isinstance(scale, Scale)
        
        # 1) Get the center point of editor
        #if it's not position we calc position of center of the screen
        if position == None:
            position = self.CalculateCenterPointOfEditor()
        
        #recalculate point to model (in mm) because we cannot scale point directly
        p3d = self.ViewToModel(position)
        scrolled_position = self.CalcScrolledPosition(position)
        
        #Calc delta between center of screen and actual position of mouse
        delta_to_screen_center = wx.Point()
        delta_to_screen_center.x = self.GetSize().x/2 - scrolled_position.x
        delta_to_screen_center.y = self.GetSize().y/2 - scrolled_position.y
        
        # 2) do scalling
        self.bounds.scale = scale
        self.SetVirtualSize(self.ComputePreferredSize())

        # 3) Move to the center of editor component
        new_position = self.ModelToView(p3d)
        #Calc center of screen including delta to screen, where is mouse
        new_screen_center_unscrolled = self.CalcUnscrolledPosition(self.CalcScrolledPosition(new_position) + delta_to_screen_center)
        
        self.CenterViewAt(new_screen_center_unscrolled)
        
        # 4) set Pen for displaying tracks
        if self.bounds.scale > 1:
            self._pen_rail_tracking_width = 3
        else:
            self._pen_rail_tracking_width = 1
        
        # 4) Refresh views
        self.Update()
        self.Refresh()
        #self.GetParent().topRuler.Refresh()
        #self.GetParent().leftRuler.Refresh()
        self.main_window.SetStatusText(str(scale), 2)
        
        
    def ViewToModel(self, point):
        """
        Converts 2D point of UI editor coordinates into 3D point
        of scenery coordinates.
        """
        return self.bounds.ViewToModel(point)


    def ModelToView(self, point = Vec3()):
        """
        Converts 3D point of scenery coordinate into 2D point of
        UI editor coordinates.
        """        
        return self.bounds.ModelToView(point)

    def CenterViewAt(self, (required_position_x, required_position_y)):
        """
        Centers the view on following point in pixels.
        """
        #gaterring necessary information
        (window_size_width, window_size_height) = self.GetSize()
        (scroll_rate_x, scroll_rate_y) = self.GetScrollPixelsPerUnit()
        
        #calculate position of left upper corner to which we scroll
        corner_x = max(0, required_position_x - (window_size_width / 2))
        corner_y = max(0, required_position_y - (window_size_height / 2))
        
        #scroll to required position
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
        """
        Computes the preferred size of the scenery size.
        """
        (w, h) = self.GetSize()        
        return self.bounds.ComputePreferredSize((w, h))


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
        
        context = ui.views.DrawContext(dc, self.bounds)

        startTime = datetime.datetime.now()
        try:
            self.PaintBackground(dc, clip, context)
            self.PaintForeground(dc, clip, context)
        finally:
            if self.logger.isEnabledFor(logging.DEBUG):
                delta = datetime.datetime.now() - startTime
                idelta = delta.days * 86400 + delta.seconds * 1000000 \
                    + delta.microseconds
                self.logger.debug(u"Paint lasted %d \u00b5s" % idelta)


    def PaintBackground(self, dc, clip, context):
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
                if (x <= xoffset):
                    dc.DrawLine(x, clip.y, x, yoffset)
            x = center2D[0]
            while x < xoffset:
                if (x >= clip.x):
                    dc.DrawLine(x, clip.y, x, yoffset)
                x = x + 100
        
            y = center2D[1]
            while y > clip.y:
                y = y - 100
                if (y <= yoffset):
                    dc.DrawLine(clip.x, y, xoffset, y)
            y = center2D[1]
            while y < yoffset:
                if (y >= clip.y):
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
        (x, y) = self.bounds.GetMinMax()

        oldPen = dc.GetPen()
        dc.SetPen(wx.Pen("#999999"))
        try:
            dc.DrawLine(clip.x, self.bounds.extentX, clip.x + clip.width, self.bounds.extentX)
            dc.DrawLine(x, clip.y, x, clip.y + clip.height)
            dc.DrawLine(clip.x, y, clip.x + clip.width, y)
            dc.DrawLine(self.bounds.extentY, clip.y, self.bounds.extentY, clip.y + clip.height)
        finally:
            dc.SetPen(oldPen)


    def PaintForeground(self, dc, clip, context):
        """
        Paints foreground
        """
        self.PaintTracks(dc, clip, context)
        self.PaintSelection(dc, clip, context)
        self.PaintSnapPoint(dc, clip, context)
        self.PaintBasePoint(dc, clip, context)
        
        
    def PaintTracks(self, dc, clip, context):
        """
        Paint rail trackings.
        """

        (vx, vy) = self.GetViewStart()
        (ux, uy) = self.GetScrollPixelsPerUnit()
        (sx, sy) = self.GetSize()

        p3a = self.ViewToModel((vx*ux, vy*uy))
        p3b = self.ViewToModel((vx*ux + sx, vy*uy + sy))
        
        viewport = sptial.Cuboid.fromEndpoints([p3a, p3b])
        elements = self.GetParent().scenery.Query(viewport)
        
        for t in elements:
            ui.views.GetViewer(t).Draw(context)
            
            
    def PaintSelection(self, dc, clip, context):
        """
        Paints rail switches.
        """
        if self.selected is not None:
            try:
                context.selected = True
                ui.views.GetViewer(self.selected).Draw(context)
            finally: 
                context.selected = False
            
            
    def PaintBasePoint(self, dc, clip, context):
        self.basePointView.Draw(context)


    def PaintSnapPoint(self, dc, clip, context):
        if self.snapData is not None:
            index = ui.views.getImageIndexByAngle(self.snapData.alpha)
            snapImage = ui.views.GetSnapPointImages()[index]

            dc.DrawBitmap(wx.BitmapFromImage(snapImage),
                self.snapData.p2d[0] - snapImage.GetWidth()/2,
                self.snapData.p2d[1] - snapImage.GetHeight()/2)


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


    def Resize(self):
        size = self.ComputePreferredSize()
        self.SetVirtualSize(size)
        self.Refresh()
        
        
    def RedrawRect(self, dirtyRegion):
        """
        Redraws the dirty region.
        Dirty region is expressed in virtual coordinates.
        """
        (vx, vy) = self.GetViewStart()
        (ux, uy) = self.GetScrollPixelsPerUnit()
        dirtyRegion.x = dirtyRegion.x - vx * ux
        dirtyRegion.y = dirtyRegion.y - vy * uy
        self.RefreshRect(dirtyRegion)




class EditorBounds:
    """
    Class holding geometry of the editor in view coordinates.
    """
    
    def __init__(self):
        self.minX = -1000.0;
        self.maxX = 1000.0;
        self.minY = -1000.0;
        self.maxY = 1000.0;
        self.scale = Scale();
        self.extentX = 100;
        self.extentY = 100;
        
    
    def ComputePreferredSize(self, actualSize):
        """
        Computes the preferred size of the scenery size.
        
        Examples:
        >>> layout = EditorBounds()
        >>> layout.ComputePreferredSize((800, 600))
        (2200, 2200)
        >>> layout.scale = Scale(SCALE_MIN)
        >>> layout.ComputePreferredSize((800, 600))
        (1000, 800)
        >>> layout.scale = Scale(SCALE_MAX)
        >>> layout.ComputePreferredSize((800, 600))
        (4000200, 4000200)
        """
        (w, h) = actualSize
        
        return (max(w, int(self.scale.get() * float(self.maxX - self.minX))) + 2 * self.extentX,
            max(h, int(self.scale.get() * float(self.maxY - self.minY))) + 2 * self.extentY)
    
    
    def ViewToModel(self, point):
        """
        Converts 2D point of UI editor coordinates into 3D point
        of scenery coordinates.
        
        Examples:
        >>> layout = EditorBounds()
        >>> layout.ViewToModel((1100, 1100))
        (0.000,0.000,0.000)
        >>> layout.scale = Scale(SCALE_MIN)
        >>> layout.ViewToModel((1100, 1100))
        (249000.000,-249000.000,0.000)
        >>> layout.scale = Scale(SCALE_MAX)
        >>> layout.ViewToModel((1100, 1100))
        (-999.500,999.500,0.000)
        """
        p3d = Vec3(Decimal(str((point[0]-self.extentX)/self.scale.get() + float(self.minX))),
            Decimal(str(-((point[1]-self.extentY)/self.scale.get() - float(self.maxY)))),
            Decimal("0"))
        return p3d


    def ModelToView(self, point = Vec3()):
        """
        Converts 3D point of scenery coordinate into 2D point of
        UI editor coordinates.
        
        Examples:
        >>> layout = EditorBounds()
        >>> layout.ModelToView()
        (1100, 1100)
        >>> layout.scale = Scale(0.5)
        >>> layout.ModelToView()
        (600, 600)
        >>> layout.scale = Scale(2.0)
        >>> layout.ModelToView()
        (2100, 2100)
        >>> layout.ModelToView(Vec3('-4.000', '540.000', '3.000'))
        (2092, 1020)
        """        
        p2d = (int((float(point.x) - float(self.minX)) * self.scale.get() + self.extentX),
            int((-float(point.y) + float(self.maxY)) * self.scale.get() + self.extentY))
        return p2d
    
    
    def GetMinMax(self):
        """
        Gets the point coordinates for max (x, y) bounds.
        
        Example:
        >>> layout = EditorBounds()
        >>> layout.GetMinMax()
        (2100, 2100)
        """
        x = int(float(self.maxX - self.minX) * self.scale.get()) + self.extentX
        y = int(float(self.maxY - self.minY) * self.scale.get()) + self.extentY
        return (x, y)
    
    
    def Update(self, point, maxPoint = None):
        """
        Updates the bounds with the cuboid and returns True if
        the bounds changed.
        
        Example:
        >>> bounds = EditorBounds()
        >>> bounds.Update((-400, -1200, 43), (1500, 800, 4))
        True
        >>> (bounds.minX, bounds.maxX, bounds.minY, bounds.maxY)
        (-1000.0, 1500.0, -1200.0, 1000.0)
        >>> bounds.Update((-200, -1100, 34), (1500, -100, 0))
        False
        >>> (bounds.minX, bounds.maxX, bounds.minY, bounds.maxY)
        (-1000.0, 1500.0, -1200.0, 1000.0)
        
        Now with single point:
        
        >>> bounds.Update((-2000, -2000))
        True
        >>> (bounds.minX, bounds.maxX, bounds.minY, bounds.maxY)
        (-2000.0, 1500.0, -2000.0, 1000.0)
        """
        if (maxPoint is not None and (maxPoint[0] < point[0] or maxPoint[1] < point[1])):
            raise ValueError            
        
        minX = min(self.minX, point[0])
        if (maxPoint is not None):
            maxX = max(self.maxX, maxPoint[0])
        else:
            maxX = max(self.maxX, point[0])
            
        minY = min(self.minY, point[1])
        if (maxPoint is not None):
            maxY = max(self.maxY, maxPoint[1])
        else:
            maxY = max(self.maxY, point[1])
        
        changed = False
        if (minX != self.minX or maxX != self.maxX or minY != self.minY or maxY != self.maxY):
            self.minX = float(minX)
            self.maxX = float(maxX)
            self.minY = float(minY)
            self.maxY = float(maxY)
            changed = True
        
        return changed
    
    
    def GetBezierFlatnessFactor(self):
        """
        Gets the flatness of Bezier approximation algorithm
        based on the scale.
        
        Example:
        >>> bounds = EditorBounds()
        >>> bounds.scale = Scale(1.0);
        >>> bounds.GetBezierFlatnessFactor()
        5
        >>> bounds.scale = Scale(0.004)
        >>> bounds.GetBezierFlatnessFactor()
        16
        >>> bounds.scale = Scale(1000.0)
        >>> bounds.GetBezierFlatnessFactor()
        3
        """
        return int(math.ceil(16 / (math.log10(self.scale.get() * 250) + 1)))
    
    
    def GetHighlightRect(self, point):
        """
        Gets the hightlight cuboid.
        
        Example:
        >>> bounds = EditorBounds()
        >>> bounds.scale = Scale(0.5)
        >>> bounds.GetHighlightRect(wx.Point(598, 602))
        [(-14.000,6.000,0.000), (6.000,-14.000,0.000)]
        """
        p2d_1 = point - wx.Point(ui.views.HIGHLIGHT_DISTANCE, ui.views.HIGHLIGHT_DISTANCE)
        p3d_1 = self.ViewToModel(p2d_1)
        p2d_2 = point + wx.Point(ui.views.HIGHLIGHT_DISTANCE, ui.views.HIGHLIGHT_DISTANCE)
        p3d_2 = self.ViewToModel(p2d_2)
        return [p3d_1, p3d_2]




class Scale:
    """
    The editor scale.

    The editor scale is defined as mathematical number set:

    .. math::
        scale = {s : s \in \Re \vee (s \geq 0.4 \vedge s \leq 2000) \vee s = 0.04 \vee s = 0.004}

    Example:
    >>> s = Scale()
    >>> s.increase()
    >>> s.get()
    2.0
    >>> s.decrease()
    >>> s.get()
    1.0
    >>> s.set(3000.0)
    Traceback (most recent call last):
        ...
    ValueError
    """

    LSCALE_MAX = 0.4

    __large_scales = [LSCALE_MAX, 0.04, SCALE_MIN]

    def __init__(self, value = SCALE_DEFAULT):
        self.set(value)


    def increase(self):
        """
        Increases a scale.

        Examples:
        >>> s = Scale()
        >>> s.increase()
        >>> s
        2px/m
        >>> s.set(0.004)
        >>> s.increase()
        >>> s
        1px/25.0m
        >>> s.increase()
        >>> s
        1px/2.5m
        >>> s.increase()
        >>> s
        1px/1.25m
        >>> s.set(1000.0)
        >>> s.increase()
        >>> s
        2000px/m
        >>> s.increase()
        >>> s
        2000px/m
        """
        try:
            idx = self.__large_scales.index(self.value)
            if (idx == 0):
                self.value = 2*self.LSCALE_MAX
            else:
                self.value = self.__large_scales[idx-1]
        except ValueError:
            n = self.value * 2
            if (n >= SCALE_MAX):
                self.value = SCALE_MAX
            else:
                self.value = n


    def decrease(self):
        """
        Decreases the scale.

        Examples:
        >>> s = Scale()
        >>> s.decrease()
        >>> s
        1px/2.0m
        >>> s.set(0.6)
        >>> s.decrease()
        >>> s
        1px/2.5m
        """
        try:
            idx = self.__large_scales.index(self.value)
            if (idx == len(self.__large_scales) - 1):
                self.value = SCALE_MIN
            else:
                self.value = self.__large_scales[idx+1]
        except ValueError:
            n = self.value / 2
            if (n <= self.LSCALE_MAX):
                self.value = self.LSCALE_MAX
            else:
                self.value = n


    def get(self):
        return self.value


    def set(self, value):
        """
        Sets the value for the scale.
        It can raise ValueError.

        Example:
        >>> s = Scale()
        >>> s.set(500.0)
        >>> s
        500px/m
        >>> s.set(2001.0)
        Traceback (most recent call last):
            ...
        ValueError
        >>> s.set(0.002)
        Traceback (most recent call last):
            ...
        ValueError
        >>> s.set(0.04)
        >>> s
        1px/25.0m
        >>> s.set(0.5)
        >>> s
        1px/2.0m
        >>> s.set(0.4)
        >>> s
        1px/2.5m
        """
        if ((value < self.LSCALE_MAX or value > SCALE_MAX) and value not in self.__large_scales):
            raise ValueError
        self.value = value


    def isLargeScale(self):
        return self.value in self.__large_scales


    def __repr__(self):
        if (self.value <= 1.0):
            return "1px/%sm" % float(1.0 / self.value)
        else:
            return "%dpx/m" % self.value




class BasePoint:
    """
    Base point.
    Defines a vector attached in some 3D world point that allows
    additions to the scenery.

    Gradient is expressed in promille's.
    """
    
    def __init__(self, p=Vec3(), alpha = 0, gradient = 0):
        self.point = p
        self.alpha = alpha
        self.gradient = gradient
        
    
    def __repr__(self):
        return u"BasePoint[point=(%.3f, %.3f, %.3f),alpha=%.2f,gradient=%.2f\u2030]" % \
           (self.point.x, self.point.y, self.point.z,
            self.alpha, self.gradient)
    
    
    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, BasePoint):
            return False
        return (self.point == other.point and self.alpha == other.alpha
                and self.gradient == other.gradient)

    def SetPosition(self, point):
        self.point = point
        
    def SetAlpha(self, alpha):
        self.alpha = alpha
        
    def SetGradient(self, gradient):
        self.gradient = gradient


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

        if self.editorPart.basePointView.IsSelectionPossible(point, self.editorPart.bounds):
            self.pressed = True
    
    
    def OnMouseRelease(self, event):
        if not self.enabled:
            return
       
        snapData = self.editorPart.snapData 
        point = self.editorPart.CalcUnscrolledPosition(event.GetPosition())
        
        if self.pressed:
            if snapData is not None:
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
            
            p2a = wx.Point(point.x - 5, point.y - 5)
            p2b = wx.Point(point.x + 5, point.y + 5)
            p3a = self.editorPart.ViewToModel(p2a)
            p3b = self.editorPart.ViewToModel(p2b)            
            
            viewport = sptial.Cuboid.fromEndpoints([p3a, p3b])
            elements = self.editorPart.GetParent().scenery.Query(viewport)
            
            for v in elements:
                foundSnapData = ui.views.GetViewer(v).GetSnapData(self.editorPart.bounds, point)
                if foundSnapData is not None:
                    self.editorPart.snapData = foundSnapData
                    break
 
            if foundSnapData is None:
                self.editorPart.snapData = None
            if oldSnapData is not None:
                self.editorPart.RedrawRect(
                    wx.Rect(oldSnapData.p2d[0]-10, oldSnapData.p2d[1]-10, 20, 20))
                updateScreen = True
            if foundSnapData is not None:
                self.editorPart.RedrawRect(
                    wx.Rect(foundSnapData.p2d[0]-10, foundSnapData.p2d[1]-10, 20, 20))
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
        rect = self.__editor.bounds.GetHighlightRect(point)
        viewport = sptial.Cuboid.fromEndpoints(rect)

        startTime = datetime.datetime.now()
        try:
            scenery = self.__editor.GetParent().GetScenery()
            
            elements = scenery.Query(viewport)
            selectedElement = next((e for e in elements if self.IsSelectionPossible(e, point)), None)
            
            if selectedElement is None:
                # Reset mode to default
                self.__editor.GetParent().SetMode(MODE_NORMAL,True)
            else:
                snapData = ui.views.GetViewer(selectedElement).GetSnapData(self.__editor.bounds, point)

                if self.__startPoint is not None:
                    # Handle second point by creating closure track and adding it to scenery
                    _trackfc = ui.trackfc.TrackFactory(self.__editor)
                    closureTrack = _trackfc.CreateClosureTrack(
                        self.__startElement, self.__startPoint, selectedElement, snapData.p3d)
                    scenery = self.__editor.GetParent().GetScenery()
                    scenery.AddRailTracking(closureTrack)

                    # Reset editor mode
                    self.__editor.GetParent().SetMode(MODE_NORMAL, True)
                else:
                    # Handle first point (store it only)
                    self.__startPoint = snapData.p3d
                    self.__startElement = selectedElement
        finally:
            delta = datetime.datetime.now() - startTime
            idelta = delta.days * 86400 + delta.seconds * 1000000 \
                + delta.microseconds
            self.__editor.logger.debug(u"Create closure track lasted %d \u00b5s" % idelta)
            
            
    def IsSelectionPossible(self, element, point):
        return ui.views.GetViewer(element).IsSelectionPossible(self.__editor.bounds, point)



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
            rect = self.editorPart.bounds.GetHighlightRect(point)
            viewport = sptial.Cuboid.fromEndpoints(rect)

            startTime = datetime.datetime.now()
            try:
                scenery = self.editorPart.GetScenery()
                elements = scenery.Query(viewport)
                selectedElement = next((e for e in elements if self.IsSelectionPossible(e, point)), None)
                self.editorPart.GetParent().SetSelection(selectedElement)
            finally:
                delta = datetime.datetime.now() - startTime
                idelta = delta.days * 86400 + delta.seconds * 1000000 + delta.microseconds
                self.editorPart.logger.debug(u"Selection lasted %d \u00b5s" % idelta)
                
                
    def IsSelectionPossible(self, element, point):
        return ui.views.GetViewer(element).IsSelectionPossible(self.editorPart.bounds, point)
    




class WheelScaler:
    """
    Responds to mouse wheel in scenery editor and adjust the scale.
    """

    def __init__(self, editor):
        self.editor = editor

    def OnMouseMove(self, event):
        self.mouse_position = event.GetPosition()
        
    def OnMouseWheel(self, event):
        delta = event.GetWheelRotation()
        mouse_logical_position_in_window = self.editor.CalcUnscrolledPosition(self.mouse_position)
                
        scale = copy.copy(self.editor.GetScale())

        if delta < 0:
            scale.decrease()
            self.editor.SetScale(scale, mouse_logical_position_in_window)
        else:
            scale.increase()
            self.editor.SetScale(scale, mouse_logical_position_in_window)
            
        event.Skip()



class SceneryListener(model.scenery.SceneryListener):
    """
    Responds to the changes in scenery
    """

    def __init__(self, editor):
        model.scenery.SceneryListener.__init__(self)
        self.editor = editor

    def Remove(self, scenery, element):
        if element == self.editor.GetSelection():
            self.editor.SetSelection(None)

        self.__refresh(scenery, element)

    def Add(self, scenery, element):
        self.__refresh(scenery, element)

    def __refresh(self, scenery, element):
        part = self.editor.parts[0]
        
        mbc = scenery.GetMbc()
        resizeNeeded = part.bounds.Update(mbc.min(), mbc.max())
        if resizeNeeded:
            part.Resize()
        else:
            box = ui.views.GetViewer(element).GetBox(part.bounds)
            part.RedrawRect(box)


if (__name__ == '__main__'):
    import doctest
    doctest.testmod()

