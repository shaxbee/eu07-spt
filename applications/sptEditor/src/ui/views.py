"""
Module containing views of scenery elements.

@author adammo
"""

import math
import os.path
import wx
from sptmath import Decimal

import model.tracks
import ui.editor
import sptmath


def loadImages(file, tiles):
    """
    Creates an array of images loaded from given PNG file.
    """
    array = []
    image = wx.Image(file, wx.BITMAP_TYPE_PNG)
    
    width = image.GetWidth() / tiles
    height = image.GetHeight()
    
    for i in xrange(tiles):
        array.append(image.GetSubImage(wx.Rect(i*width, 0, width, height)))
        
    return array


def getImageIndexByAngle(angle):
    """
    Gets the image index for basepoint, snappoint alpha angle.
    
    Examples:
    >>> import math
    >>> map(getImageIndexByAngle, [0.0, 180.0, 90.0, 270.0, -3.0, -2.4, -2.5, 2.4, 2.5, 45.0, 357.613626644])
    [0, 36, 18, 54, 71, 0, 0, 0, 1, 9, 0]
    """
    d = math.radians(angle + 2.5)
    if d < 0.0:
        d = d + 2*math.pi
    d = d / (2*math.pi)
    index = int(d * 72)
    return 0 if index > 71 else index




BASEPOINT_IMAGES = None
SNAP_BASEPOINT_IMAGES = None


def GetBasePointImages():
    global BASEPOINT_IMAGES
    if BASEPOINT_IMAGES is None:
        BASEPOINT_IMAGES = loadImages(os.path.join("icons", "canvas", "basepoint.png"), 72)
    return BASEPOINT_IMAGES


def GetSnapPointImages():
    global SNAP_BASEPOINT_IMAGES
    if SNAP_BASEPOINT_IMAGES is None:
        SNAP_BASEPOINT_IMAGES = loadImages(os.path.join("icons", "canvas", "snappoint.png"), 72)
    return SNAP_BASEPOINT_IMAGES


SNAP_DISTANCE_SQ = 25
HIGHLIGHT_DISTANCE = 5
HIGHLIGHT_DISTANCE_SQ = HIGHLIGHT_DISTANCE * HIGHLIGHT_DISTANCE

COLOR_TRACK = (34, 139, 34)
COLOR_SWITCH = (173, 255, 47)
COLOR_HIGHLIGHT = (255, 0, 0)




class Snapable:
    """
    An interface telling that view is snappable.
    """
    
    def GetSnapData(self, point, context):
        """
        For given editor point returns snap data object if snap is possible
        for the point or not.
        """
        pass # Implement it




class DrawContext:
    """
    Draw context contains the all information to
    draw the scenery element onto editor pane.
    """
    
    def __init__(self, dc, bounds, selected = False):
        self.dc = dc
        self.bounds = bounds
        self.selected = selected



class TrackViewer:
    
    def __init__(self, track):
        self.track = track
    
    
    def Draw(self, context):
        """
        Draws the track on the device context.
        """
        
        oldPen = context.dc.GetPen()
        try:
            context.dc.SetPen(wx.Pen(COLOR_TRACK if not context.selected else COLOR_HIGHLIGHT,
                3 if context.bounds.scale > 1.0 else 1))
        
            if (context.bounds.scale.isLargeScale()):
                p1 = context.bounds.ModelToView(self.track.p1)
                p2 = context.bounds.ModelToView(self.track.p2)
                
                context.dc.DrawLine(p1[0], p1[1], p2[0], p2[1])
            else:
                spline = (context.bounds.ModelToView(self.track.p1),
                          context.bounds.ModelToView(self.track.p1 + self.track.v1),
                          context.bounds.ModelToView(self.track.p2 + self.track.v2),
                          context.bounds.ModelToView(self.track.p2))
            
                context.dc.DrawSpline(spline)
        finally:
            context.dc.SetPen(oldPen)
            
            
    def GetBox(self, bounds):
        """
        Gets the rectangle for the track.
        
        Examples:
        >>> from model.tracks import Track
        >>> from editor import EditorBounds, Scale
        >>> from sptmath import Vec3
        >>> t = Track(p1 = Vec3("-51416.636", "56806.718", "0.000"),
        ...     v1 = Vec3("-1.416", "-16.607", "0.000"),
        ...     v2 = Vec3("0.376", "16.664", "0.000"),
        ...     p2 = Vec3("-51419.325", "56756.799", "0.000"))
        >>> bounds = EditorBounds()
        >>> bounds.scale = Scale(10.0)
        >>> bounds.minX = -60000.0
        >>> bounds.maxX = 1000.0
        >>> bounds.minY = -1000.0
        >>> bounds.maxY = 60000.0
        >>> tv = TrackViewer(t)
        >>> tv.GetBox(bounds)
        wx.Rect(85906, 32032, 28, 500)
        """
        p1 = bounds.ModelToView(self.track.p1)
        v1 = bounds.ModelToView(self.track.p1 + self.track.v1)
        v2 = bounds.ModelToView(self.track.p2 + self.track.v2)
        p2 = bounds.ModelToView(self.track.p2)
        
        left = min(p1[0], v1[0], v2[0], p2[0])
        right = max(p1[0], v1[0], v2[0], p2[0])
        top = min(p1[1], v1[1], v2[1], p2[1])        
        bottom = max(p1[1], v1[1], v2[1], p2[1])
        
        return wx.Rect(left, top, right-left+1, bottom-top+1)
    
    
    def GetSnapData(self, bounds, point):
        """
        Gets the snap data for this view.
        
        Example:
        >>> from model.tracks import Track
        >>> from editor import EditorBounds, Scale 
        >>> from sptmath import Vec3
        >>> import wx
        >>> t = Track(p1 = Vec3("-51416.636", "56806.718", "0.000"),
        ...     v1 = Vec3("-1.416", "-16.607", "0.000"),
        ...     v2 = Vec3("0.376", "16.664", "0.000"),
        ...     p2 = Vec3("-51419.325", "56756.799", "0.000"))
        >>> bounds = EditorBounds()
        >>> bounds.scale = Scale(10.0)
        >>> bounds.minX = -55000.0
        >>> bounds.maxX = 1000.0
        >>> bounds.minY = -5000.0
        >>> bounds.maxY = 60000.0
        >>> tv = TrackViewer(t)
        >>> sp = tv.GetSnapData(bounds, wx.Point(35935, 32030))
        >>> sp.p2d
        (35933, 32032)
        >>> sp.p3d
        (-51416.636,56806.718,0.000)
        >>> round(sp.alpha, 2)
        4.87
        >>> sp = tv.GetSnapData(bounds, wx.Point(35907, 32530))
        >>> sp.p2d
        (35906, 32531)
        >>> sp.p3d
        (-51419.325,56756.799,0.000)
        >>> round(sp.alpha, 2)
        -178.71
        >>> tv.GetSnapData(bounds, wx.Point(0, 0))
        
        """
        p1 = bounds.ModelToView(self.track.p1)
        p2 = bounds.ModelToView(self.track.p2)
        
        p1x = p1[0] - point.x
        p1y = p1[1] - point.y
        p2x = p2[0] - point.x
        p2y = p2[1] - point.y
        if (p1x * p1x + p1y * p1y <= SNAP_DISTANCE_SQ
                and self.track.point2tracking(self.track.p1) == None):

            data = ui.editor.SnapData()
            data.p2d = p1
            data.p3d = self.track.p1
            data.Complete(self.track)
            return data
        elif (p2x * p2x + p2y * p2y <= SNAP_DISTANCE_SQ
                and self.track.point2tracking(self.track.p2) == None):
            data = ui.editor.SnapData()
            data.p2d = p2
            data.p3d = self.track.p2
            data.Complete(self.track)
            return data
        else:
            return None
        
        
    def IsSelectionPossible(self, bounds, point):
        """
        Returns True if selection is possible.
        
        Example:
        >>> from model.tracks import Track
        >>> from editor import EditorBounds, Scale
        >>> from sptmath import Vec3
        >>> import wx
        >>> t = Track(p1 = Vec3("-51416.636", "56806.718", "0.000"),
        ...     v1 = Vec3("-1.416", "-16.607", "0.000"),
        ...     v2 = Vec3("0.376", "16.664", "0.000"),
        ...     p2 = Vec3("-51419.325", "56756.799", "0.000"))
        >>> bounds = EditorBounds()
        >>> bounds.scale = Scale(10.0)
        >>> bounds.minX = -55000.0
        >>> bounds.maxX = 1000.0
        >>> bounds.minY = -5000.0
        >>> bounds.maxY = 60000.0
        >>> tv = TrackViewer(t)
        >>> tv.IsSelectionPossible(bounds, wx.Point(35935, 32030))
        True
        >>> tv.IsSelectionPossible(bounds, wx.Point(35950, 32048))
        False
        """
        p1 = bounds.ModelToView(self.track.p1)
        v1 = bounds.ModelToView(self.track.p1 + self.track.v1)
        v2 = bounds.ModelToView(self.track.p2 + self.track.v2)
        p2 = bounds.ModelToView(self.track.p2)

        lines = sptmath.toLineSegments((p1, v1, v2, p2), bounds.GetBezierFlatnessFactor())
        i = 1
        while i < len(lines):
            l = lines[i-1:i+1]
            if sptmath.sqDistanceTo(l, point) <= HIGHLIGHT_DISTANCE_SQ:
                return True
            i += 1
        return False
            
        
        
        
class SwitchViewer:
    
    def __init__(self, switch):
        self.switch = switch
        
    
    def Draw(self, context):
        """
        Draws the switch on the device context.
        """
        
        oldPen = context.dc.GetPen()
        try:
            context.dc.SetPen(wx.Pen(COLOR_SWITCH if not context.selected else COLOR_HIGHLIGHT,
                3 if context.bounds.scale > 1.0 else 1))
            
            if (context.bounds.scale.isLargeScale()):
                pc = context.bounds.ModelToView(self.switch.pc)
                p1 = context.bounds.ModelToView(self.switch.p1)
                p2 = context.bounds.ModelToView(self.switch.p2)
                
                context.dc.DrawLine(pc[0], pc[1], p1[0], p1[1])
                context.dc.DrawLine(pc[0], pc[1], p2[0], p2[1])
            else:
                s = (context.bounds.ModelToView(self.switch.pc),
                     context.bounds.ModelToView(self.switch.pc + self.switch.vc1),
                     context.bounds.ModelToView(self.switch.p1 + self.switch.v1),
                     context.bounds.ModelToView(self.switch.p1))
                d = (context.bounds.ModelToView(self.switch.pc),
                     context.bounds.ModelToView(self.switch.pc + self.switch.vc2),
                     context.bounds.ModelToView(self.switch.p2 + self.switch.v2),
                     context.bounds.ModelToView(self.switch.p2))
            
                context.dc.DrawSpline(s)
                context.dc.DrawSpline(d)
        finally:
            context.dc.SetPen(oldPen)
            
    
    def GetBox(self, bounds):
        """
        Gets the rectangle for the switch.
        
        Examples:
        >>> from model.tracks import Switch
        >>> from editor import EditorBounds, Scale
        >>> from sptmath import Vec3
        >>> s = Switch(
        ...     pc = Vec3("-51425.436", "56655.860", "0.000"),        
        ...     p1 = Vec3("-51434.064", "56591.618", "0.000"),
        ...     p2 = Vec3("-51435.794", "56591.883", "0.000"),
        ...     vc1 = Vec3("0.000", "0.000", "0.000"),     
        ...     v1 = Vec3("0.000", "0.000", "0.000"),
        ...     vc2 = Vec3("-2.876", "-21.415", "0.000"),        
        ...     v2 = Vec3("4.028", "21.228", "0.000"))        
        >>> bounds = EditorBounds()
        >>> bounds.scale = Scale(0.8)
        >>> bounds.minX = -60000.0
        >>> bounds.maxX = 1000.0
        >>> bounds.minY = -1000.0
        >>> bounds.maxY = 60000.0
        >>> sw = SwitchViewer(s)
        >>> sw.GetBox(bounds)
        wx.Rect(6951, 2775, 9, 52)
        """
        pc = bounds.ModelToView(self.switch.pc)
        vc1 = bounds.ModelToView(self.switch.pc + self.switch.vc1)
        v1 = bounds.ModelToView(self.switch.p1 + self.switch.v1)
        p1 = bounds.ModelToView(self.switch.p1)
        vc2 = bounds.ModelToView(self.switch.pc + self.switch.vc2)
        v2 = bounds.ModelToView(self.switch.p2 + self.switch.v2)
        p2 = bounds.ModelToView(self.switch.p2)
        
        left = min(pc[0], vc1[0], v1[0], p1[0], vc2[0], v2[0], p2[0])
        right = max(pc[0], vc1[0], v1[0], p1[0], vc2[0], v2[0], p2[0])
        top = min(pc[1], vc1[1], v1[1], p1[1], vc2[1], v2[1], p2[1])
        bottom = max(pc[1], vc1[1], v1[1], p1[1], vc2[1], v2[1], p2[1])
        
        return wx.Rect(left, top, right-left+1, bottom-top+1)
    
    
    def GetSnapData(self, bounds, point):
        """
        Gets the snap data for this view.
        
        Example:
        >>> from model.tracks import Switch
        >>> from editor import EditorBounds, Scale
        >>> from sptmath import Vec3
        >>> import wx
        >>> s = Switch(pc = Vec3("-51416.636", "56806.718", "0.000"),
        ...     p1 = Vec3("-51412.000", "56755.000", "0.000"),
        ...     vc1 = Vec3("-1.416", "-16.607", "0.000"),
        ...     v2 = Vec3("0.376", "16.664", "0.000"),
        ...     p2 = Vec3("-51419.325", "56756.799", "0.000"))
        >>> bounds = EditorBounds()
        >>> bounds.scale = Scale(10.0)
        >>> bounds.minX = -55000.0
        >>> bounds.maxX = 1000.0
        >>> bounds.minY = -5000.0
        >>> bounds.maxY = 60000.0
        >>> tv = SwitchViewer(s)
        >>> sp = tv.GetSnapData(bounds, wx.Point(35935, 32030))
        >>> sp.p2d
        (35933, 32032)
        >>> sp.p3d
        (-51416.636,56806.718,0.000)
        >>> round(sp.alpha, 2)
        4.87
        >>> sp = tv.GetSnapData(bounds, wx.Point(35907, 32530))
        >>> sp.p2d
        (35906, 32531)
        >>> sp.p3d
        (-51419.325,56756.799,0.000)
        >>> round(sp.alpha, 2)
        -178.71
        >>> tv.GetSnapData(bounds, wx.Point(0, 0))
        
        """
        pc = bounds.ModelToView(self.switch.pc)
        p1 = bounds.ModelToView(self.switch.p1)
        p2 = bounds.ModelToView(self.switch.p2)        
        
        pcx = pc[0] - point.x
        pcy = pc[1] - point.y
        p1x = p1[0] - point.x
        p1y = p1[1] - point.y
        p2x = p2[0] - point.x
        p2y = p2[1] - point.y
        if (pcx * pcx + pcy * pcy <= SNAP_DISTANCE_SQ
            and self.switch.point2tracking(self.switch.pc) is None):
            
            data = ui.editor.SnapData()
            data.p2d = pc
            data.p3d = self.switch.pc
            data.Complete(self.switch)
            return data
        elif (p1x * p1x + p1y * p1y <= SNAP_DISTANCE_SQ
                and self.switch.point2tracking(self.switch.p1) is None):

            data = ui.editor.SnapData()
            data.p2d = p1
            data.p3d = self.switch.p1
            data.Complete(self.switch)
            return data
        elif (p2x * p2x + p2y * p2y <= SNAP_DISTANCE_SQ
                and self.switch.point2tracking(self.switch.p2) is None):
            data = ui.editor.SnapData()
            data.p2d = p2
            data.p3d = self.switch.p2
            data.Complete(self.switch)
            return data
        else:
            return None
        
        
        
    def IsSelectionPossible(self, bounds, point):
        """
        Returns True if selection is possible
        
        Example:
        >>> from model.tracks import Switch
        >>> from editor import EditorBounds, Scale
        >>> from sptmath import Vec3
        >>> import wx
        >>> s = Switch(pc = Vec3("-51416.636", "56806.718", "0.000"),
        ...     p1 = Vec3("-51412.000", "56755.000", "0.000"),
        ...     vc1 = Vec3("-1.416", "-16.607", "0.000"),
        ...     v2 = Vec3("0.376", "16.664", "0.000"),
        ...     p2 = Vec3("-51419.325", "56756.799", "0.000"))
        >>> bounds = EditorBounds()
        >>> bounds.scale = Scale(10.0)
        >>> bounds.minX = -55000.0
        >>> bounds.maxX = 1000.0
        >>> bounds.minY = -5000.0
        >>> bounds.maxY = 60000.0
        >>> tv = SwitchViewer(s)
        >>> tv.IsSelectionPossible(bounds, wx.Point(35935, 32030))
        True
        >>> tv.IsSelectionPossible(bounds, wx.Point(35935, 33030))
        False
        """
        pc = bounds.ModelToView(self.switch.pc)
        vc1 = bounds.ModelToView(self.switch.pc + self.switch.vc1)
        v1 = bounds.ModelToView(self.switch.p1 + self.switch.v1)
        p1 = bounds.ModelToView(self.switch.p1)
        vc2 = bounds.ModelToView(self.switch.pc + self.switch.vc2)
        v2 = bounds.ModelToView(self.switch.p2 + self.switch.v2)
        p2 = bounds.ModelToView(self.switch.p2)

        flatnessFactor = bounds.GetBezierFlatnessFactor()

        lines = sptmath.toLineSegments((pc, vc1, v1, p1), flatnessFactor)
        i = 1
        while i < len(lines):
            l = lines[i-1:i+1]
            if sptmath.sqDistanceTo(l, point) <= HIGHLIGHT_DISTANCE_SQ:
                return True
            i += 1
        
        lines = sptmath.toLineSegments((pc, vc2, v2, p2), flatnessFactor)
        i = 1
        while i < len(lines):
            l = lines[i-1:i+1]
            if sptmath.sqDistanceTo(l, point) <= HIGHLIGHT_DISTANCE_SQ:
                return True
            i += 1

        return False;




class GroupViewer:
    
    def __init__(self, group):
        self.group = group
        
        
    def Draw(self, context):
        """
        Draw the rail container.
        """
        for c in self.group.children:
            GetViewer(c).Draw(context)
            
            
    def GetBox(self, bounds):
        """
        Gets the rectangle for this group.
        
        Example:
        >>> from model.groups import RailContainer
        >>> from model.tracks import Track
        >>> from model.tracks import Switch
        >>> from sptmath import Vec3
        >>> from editor import EditorBounds, Scale 
        >>> s = Switch(
        ...     pc = Vec3("-51396.960", "57230.386", "0.000"),        
        ...     p1 = Vec3("-51390.226", "57262.927", "0.000"),
        ...     p2 = Vec3("-51388.440", "57262.487", "0.000"),
        ...     vc1 = Vec3("0.000", "0.000", "0.000"),
        ...     v1 = Vec3("0.000", "0.000", "0.000"),
        ...     vc2 = Vec3("2.245", "10.849", "0.000"),    
        ...     v2 = Vec3("-3.431", "-10.535", "0.000"))
        >>> t = Track(
        ...    p1 = Vec3("-51365.143", "57357.608", "0.000"),
        ...    p2 = Vec3("-51375.385", "57326.014", "0.000"),
        ...    v1 = Vec3("-3.994", "-10.334", "0.000"),
        ...    v2 = Vec3("2.828", "10.713", "0.000"))
        >>> g = RailContainer()
        >>> g.insert(s)
        >>> g.insert(t)
        >>> bounds = EditorBounds()
        >>> bounds.scale = Scale(2.0)
        >>> bounds.minX = -100000.0
        >>> bounds.maxX = 1000.0
        >>> bounds.minY = -100000.0
        >>> bounds.maxY = 60000.0
        >>> gv = GroupViewer(g)
        >>> gv.GetBox(bounds)
        wx.Rect(97306, 5640, 65, 257)
        """
        mbc = self.group.children.getMbc()
        
        min = bounds.ModelToView(mbc.min())
        max = bounds.ModelToView(mbc.max())
        
        return wx.Rect(min[0], min[1], max[0]-min[0]+1, min[1]-max[1]+1)


    def GetSnapData(self, bounds, point):
        """
        Gets the snap data for this view.
        """
        for c in self.group.children:
            sd = GetViewer(c).GetSnapData(bounds, point)
            if sd is not None:
                return sd
        return None
    
    
    def IsSelectionPossible(self, bounds, point):
        """
        Iterates through the children to search potential selection.
        """
        for c in self.group.children:
            if (GetViewer(c).IsSelectionPossible(bounds, point)):
                return True
        return False



class BasePointView:
    """
    A view for base point.
    """
    
    def __init__(self, basePoint):
        self.basePoint = ui.editor.BasePoint(basePoint.point, basePoint.alpha, basePoint.gradient)

    
    def Draw(self, context):
        p2d = context.bounds.ModelToView(self.basePoint.point)
        index = getImageIndexByAngle(self.basePoint.alpha)
        image = GetBasePointImages()[index]
        context.dc.DrawBitmap(wx.BitmapFromImage(image), \
                      p2d[0] - image.GetWidth() / 2, \
                      p2d[1] - image.GetHeight() / 2)
        
        
    def GetBox(self, bounds):
        """
        Returns the box for base point.
        
        Examples:
        >>> from ui.editor import BasePoint, EditorBounds, Scale
        >>> from sptmath import Vec3
        >>> bp = BasePoint(Vec3('-787.343', '34.342', '-23.005'), 1.0, 0.0)
        >>> bounds = EditorBounds()
        >>> bounds.scale = Scale(2.0)
        >>> bounds.minX = -100000.0
        >>> bounds.maxX = 1000.0
        >>> bounds.minY = -100000.0
        >>> bounds.maxY = 60000.0
        >>> bv = BasePointView(bp)
        >>> bv.GetBox(bounds)
        wx.Rect(198515, 120021, 20, 20)
        """
        p2d = bounds.ModelToView(self.basePoint.point)
        return wx.Rect(p2d[0] - 10, p2d[1] - 10, 20, 20)
    
    
    def IsSelectionPossible(self, point, bounds):
        """
        Checks if selection of this view is possible from given point.
        """
        p2d = bounds.ModelToView(self.basePoint.point)
        x = p2d[0] - point.x
        y = p2d[1] - point.y
        return (x*x + y*y) <= SNAP_DISTANCE_SQ




def GetViewer(element):
    """
    Factory for viewers.
    """
    if (isinstance(element, model.tracks.Track)):
        return TrackViewer(element)
    elif (isinstance(element, model.tracks.Switch)):
        return SwitchViewer(element)
    elif (isinstance(element, model.groups.RailContainer)):
        return GroupViewer(element)
    else:
        raise ValueError(element)
