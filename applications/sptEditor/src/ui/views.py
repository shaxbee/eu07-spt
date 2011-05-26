"""
Module containing views of scenery elements.

@author adammo
"""

import math
import os.path
import wx
from decimal import Decimal

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
    d = math.radians(angle + 2.5)
    if d < 0.0:
        d += 2*math.pi
    d = d / (2*math.pi)
    return int(d * 72)


BASEPOINT_IMAGES = loadImages(os.path.join( \
    "icons", "canvas", "basepoint.png"), 72)
SNAP_BASEPOINT_IMAGES = loadImages(os.path.join( \
    "icons", "canvas", "snappoint.png"), 72)

SNAP_DISTANCE = 25

COLOR_TRACK = (34, 139, 34)
COLOR_SWITCH = (173, 255, 47)




# TODO: check if this is still needed
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
    
    def __init__(self, dc, bounds):
        self.dc = dc
        self.bounds = bounds



class TrackViewer:
    
    def __init__(self, track):
        self.track = track
    
    
    def Draw(self, context):
        """
        Draws the track on the device context.
        """
        
        oldPen = context.dc.GetPen()
        try:
            context.dc.SetPen(wx.Pen(COLOR_TRACK,
                3 if context.bounds.scale > 1.0 else 1))
        
            if (context.bounds.scale < 1.0):
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
        >>> from editor import EditorBounds
        >>> from sptmath import Vec3
        >>> t = Track(p1 = Vec3("-51416.636", "56806.718", "0.000"),
        ...     v1 = Vec3("-1.416", "-16.607", "0.000"),
        ...     v2 = Vec3("0.376", "16.664", "0.000"),
        ...     p2 = Vec3("-51419.325", "56756.799", "0.000"))
        >>> bounds = EditorBounds()
        >>> bounds.scale = 10.0
        >>> bounds.minX = -60000.0
        >>> bounds.maxX = 1000.0
        >>> bounds.minY = -1000.0
        >>> bounds.maxY = 60000.0
        >>> tv = TrackViewer(t)
        >>> tv.GetBox(bounds)
        wx.Rect(85906, 32032, 28, 501)
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
        
        
        
class SwitchViewer:
    
    def __init__(self, switch):
        self.switch = switch
        
    
    def Draw(self, context):
        """
        Draws the switch on the device context.
        """
        
        oldPen = context.dc.GetPen()
        try:
            context.dc.SetPen(wx.Pen(COLOR_SWITCH,
                3 if context.bounds.scale > 1.0 else 1))
            
            if (context.bounds.scale < 1.0):
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
        >>> from editor import EditorBounds
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
        >>> bounds.scale = 0.5
        >>> bounds.minX = -60000.0
        >>> bounds.maxX = 1000.0
        >>> bounds.minY = -1000.0
        >>> bounds.maxY = 60000.0
        >>> sw = SwitchViewer(s)
        >>> sw.GetBox(bounds)
        wx.Rect(4382, 1772, 6, 33)
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
        >>> from editor import EditorBounds        
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
        >>> bounds.scale = 2
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



class BasePointView:
    """
    A view for base point.
    """
    
    def __init__(self, basePoint):
        self.basePoint = basePoint
        self.point = wx.Point()

    
    def GetElement(self):
        return self.basePoint
    
    
    def GetMinMax(self):
        x = float(self.basePoint.point.x)
        y = float(self.basePoint.point.y)
   	return (x, x, y, y) 
    
    def Scale(self, scale, oMinX, oMaxX, oMinY, oMaxY):
        self.point.x = int(((float(self.basePoint.point.x) - oMinX) * scale) + 100)
        self.point.y = int(((-float(self.basePoint.point.y) + oMaxY) * scale) + 100)


    def Draw(self, dc, clip, context):
        index = getImageIndexByAngle(self.basePoint.alpha)
        dc.DrawBitmap(wx.BitmapFromImage(BASEPOINT_IMAGES[index]), \
                      self.point.x - BASEPOINT_IMAGES[index].GetWidth() / 2, \
                      self.point.y - BASEPOINT_IMAGES[index].GetHeight() / 2)
        
        
    def GetRepaintBounds(self, context):
        return wx.Rect(self.point.x - 10, self.point.y - 10, 20, 20)
    
    
    def IsSelectionPossible(self, point, context):
        """
        Checks if selection of this view is possible from given point.
        """
        x = self.point.x - point.x
        y = self.point.y - point.y
        return (x*x + y*y) <= SNAP_DISTANCE




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
