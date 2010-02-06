"""
Module containing views of scenery elements.

@author adammo
"""

import math
import wx
from decimal import Decimal

import model.tracks
import ui.editor


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


BASEPOINT_IMAGES = loadImages("basepoint.png", 72)

SNAP_DISTANCE = 25



class View:
    """
    Abstract class defining a view.
    """

    def GetObject(self):
        """
        Gets the model object for this view.
        """
        pass # Implement it
    
    
    def Scale(self, scale, oMinX, oMaxX, oMinY, oMaxY):
        """
        Scales the view.
        """
        pass # Implement it
    
    
    def GetMinMax(self):
        """
        Gets the tuple of min max information.
        
        Returing tuple has following values (minX, maxX, minY, maxY). 
        """
        pass # Implement it
    
    
    def Draw(self, dc, clip):
        """
        Draws the view on given DeviceContext and clipping by clip rectangle.
        """
        pass # Implement it
    
    
    def GetRepaintBounds(self):
        """
        Returns the bounds (rectangle) that this view occupies.
        """
        pass # Implement it




class Snapable:
    """
    An instarface telling that view is snappable.
    """
    
    def GetSnapData(self, point):
        """
        For given editor point returns snap data object if snap is possible
        for the point or not.
        """
        pass # Implement it



    
class TrackView(View, Snapable):
    """
    View implementation for track.
    """
    
    def __init__(self, track):
        self.track = track
        self.curve = [wx.Point(0.0, 0.0), wx.Point(0.0, 0.0), \
                      wx.Point(0.0, 0.0), wx.Point(0.0, 0.0)]
        
        
    def GetElement(self):
        return self.track
    
    
    def GetMinMax(self):
        xspan = [self.track.p1.x, self.track.p2.x, \
                     self.track.p1.x + self.track.v1.x, \
                     self.track.p2.x + self.track.v2.x]
        yspan = [self.track.p1.y, self.track.p2.y, \
                     self.track.p1.y + self.track.v1.y, \
                     self.track.p2.y + self.track.v2.y]
        return (float(min(xspan)), float(max(xspan)), float(min(yspan)), float(max(yspan))) 
    
    
    def Scale(self, scale, oMinX, oMaxX, oMinY, oMaxY):
        factor = float(scale / ui.editor.SCALE_FACTOR)
        
        self.curve[0].x = (float(self.track.p1.x) - oMinX) * factor + 100
        self.curve[0].y = (-float(self.track.p1.y) + oMaxY) * factor + 100
        self.curve[3].x = (float(self.track.p2.x) - oMinX) * factor + 100
        self.curve[3].y = (-float(self.track.p2.y) + oMaxY) * factor + 100
        
        self.curve[1].x = (float(self.track.p1.x) + float(self.track.v1.x) - oMinX) \
            * factor + 100;
        self.curve[1].y = (-float(self.track.p1.y) - float(self.track.v1.y) + oMaxY) \
            * factor + 100;
        self.curve[2].x = (float(self.track.p2.x) + float(self.track.v2.x) - oMinX) \
            * factor + 100;
        self.curve[2].y = (-float(self.track.p2.y) - float(self.track.v2.y) + oMaxY) \
            * factor + 100;        
        
    
    def Draw(self, dc, clip):
        dc.DrawSpline(self.curve)


    def GetRepaintBounds(self):
        xspan = [self.curve[0].x, self.curve[1].x, \
                 self.curve[2].x, self.curve[3].x]
        yspan = [self.curve[0].y, self.curve[1].y, \
                 self.curve[2].y, self.curve[3].y]
        l = min(xspan)
        r = max(xspan)
        t = min(yspan)
        b = max(yspan)
        return wx.Rect(l, t, r-l, b-t)


    def GetSnapData(self, point):
        p1x = self.curve[0].x - point.x
        p1y = self.curve[0].y - point.y
        p2x = self.curve[3].x - point.x
        p2y = self.curve[3].y - point.y
        if p1x * p1x + p1y * p1y <= SNAP_DISTANCE:
            data = ui.editor.SnapData()
            data.p2d = self.curve[0]
            data.p3d = self.track.p1
        elif p2x * p2x + p2y * p2y <= SNAP_DISTANCE:
            data = ui.editor.SnapData()
            data.p2d = self.curve[3]
            data.p3d = self.track.p2
        else:
            return None




class RailSwitchView(View):
    """
    View implementation for rail switches.
    """
    
    def __init__(self, switch):
        self.switch = switch
        self.straight = [wx.Point(0.0, 0.0), wx.Point(0.0, 0.0), \
                         wx.Point(0.0, 0.0), wx.Point(0.0, 0.0)]
        self.diverging = [wx.Point(0.0, 0.0), wx.Point(0.0, 0.0), \
                          wx.Point(0.0, 0.0), wx.Point(0.0, 0.0)]
        
    
    def GetElement(self):
        return self.switch
    
    
    def GetMinMax(self):
        xspan = [self.switch.p1.x, self.switch.p2.x, \
                     self.switch.p1.x + self.switch.v1.x, \
                     self.switch.p2.x + self.switch.v2.x, \
                     self.switch.pc.x, \
                     self.switch.pc.x + self.switch.vc1.x, \
                     self.switch.pc.x + self.switch.vc2.x]
        yspan = [self.switch.p1.y, self.switch.p2.y, \
                     self.switch.p1.y + self.switch.v1.y, \
                     self.switch.p2.y + self.switch.v2.y, \
                     self.switch.pc.y, \
                     self.switch.pc.y + self.switch.vc1.y, \
                     self.switch.pc.y + self.switch.vc2.y]
        return (float(min(xspan)), float(max(xspan)), float(min(yspan)), float(max(yspan)))
    
    
    def Scale(self, scale, oMinX, oMaxX, oMinY, oMaxY):
        factor = float(scale / ui.editor.SCALE_FACTOR);
      
        self.straight[0].x = (float(self.switch.pc.x) - oMinX) * factor + 100;
        self.straight[0].y = (-float(self.switch.pc.y) + oMaxY) * factor + 100;
        self.straight[3].x = (float(self.switch.p1.x) - oMinX) * factor + 100;
        self.straight[3].y = (-float(self.switch.p1.y) + oMaxY) * factor + 100;
      
        self.straight[1].x = (float(self.switch.pc.x) + float(self.switch.vc1.x)-oMinX) \
            * factor + 100;
        self.straight[1].y = (-float(self.switch.pc.y) - float(self.switch.vc1.y)+oMaxY) \
            * factor + 100;
        self.straight[2].x = (float(self.switch.p1.x) + float(self.switch.v1.x)-oMinX) \
            * factor + 100;
        self.straight[2].y = (-float(self.switch.p1.y) - float(self.switch.v1.y)+oMaxY) \
            * factor + 100;
      
        self.diverging[0].x = (float(self.switch.pc.x) - oMinX) * factor + 100;
        self.diverging[0].y = (-float(self.switch.pc.y) + oMaxY) * factor + 100;
        self.diverging[3].x = (float(self.switch.p2.x) - oMinX) * factor + 100;
        self.diverging[3].y = (-float(self.switch.p2.y) + oMaxY) * factor + 100;
      
        self.diverging[1].x = (float(self.switch.pc.x) + float(self.switch.vc2.x)-oMinX) \
            * factor + 100;
        self.diverging[1].y = (-float(self.switch.pc.y) - float(self.switch.vc2.y)+oMaxY) \
            * factor + 100;
        self.diverging[2].x = (float(self.switch.p2.x) + float(self.switch.v2.x)-oMinX) \
            * factor + 100;
        self.diverging[2].y = (-float(self.switch.p2.y) - float(self.switch.v2.y)+oMaxY) \
            * factor + 100;
    
    
    def Draw(self, dc, clip):
        dc.DrawSpline(self.straight)
        dc.DrawSpline(self.diverging)
        
        
    def GetRepaintBounds(self):
        xspan = [self.straight[0].x, self.straight[1].x, \
                 self.straight[2].x, self.straight[3].x, \
                 self.diverging[0].x, self.diverging[1].x, \
                 self.diverging[2].x, self.diverging[3].x]
        yspan = [self.straight[0].y, self.straight[1].y, \
                 self.straight[2].y, self.straight[3].y, \
                 self.diverging[0].y, self.diverging[1].y, \
                 self.diverging[2].y, self.diverging[3].y]
        l = min(xspan)
        r = max(xspan)
        t = min(yspan)
        b = max(yspan)
        return wx.Rect(l, t, r-l, b-t)




class BasePointView(View):
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
        factor = float(scale / ui.editor.SCALE_FACTOR)
        
        self.point.x = int(((float(self.basePoint.point.x) - oMinX) * factor) + 100)
        self.point.y = int(((-float(self.basePoint.point.y) + oMaxY) * factor) + 100)


    def Draw(self, dc, clip):
        index = self.__GetAngleIndex()        
        dc.DrawBitmap(wx.BitmapFromImage(BASEPOINT_IMAGES[index]), \
                      self.point.x - BASEPOINT_IMAGES[index].GetWidth() / 2, \
                      self.point.y - BASEPOINT_IMAGES[index].GetHeight() / 2)
        
        
    def __GetAngleIndex(self):
        d = math.radians(self.basePoint.alpha) + math.radians(2.5)
        if d < 0.0:
            d += 2 * math.pi
        d /= 2 * math.pi
        return int(d * 72)
    
    
    def GetRepaintBounds(self):
        return wx.Rect(self.point.x - 10, self.point.y - 10, 20, 20)
    
    
    def IsSelectionPossible(self, point):
        """
        Checks if selection of this view is possible from given point.
        """
        x = self.point.x - point.x
        y = self.point.y - point.y
        return (x*x + y*y) <= SNAP_DISTANCE




def CreateView(element):
    """
    Creates view.
    """
    if type(element) == model.tracks.Track:
        return TrackView(element)
    elif type(element) == model.tracks.Switch:
        return SwitchView(switch)
    else:
        raise ValueError("Unsupported element: " + str(type(element)))

