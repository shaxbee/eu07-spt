"""
Module containing views of scenery elements.

@author adammo
"""

import math
import wx

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




class View:
    """
    Abstract class defining a view.
    """

    def GetObject(self):
        """
        Gets the model object for this view.
        """
        pass # Implement it
    
    
    def Scale(self, scale, minmax):
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
    
    
    
    
class TrackView(View):
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
        xspan = [self.track.p1[0], self.track.p2[0], \
                     self.track.p1[0] + self.track.v1[0], \
                     self.track.p2[0] + self.track.v2[0]]
        yspan = [self.track.p1[1], self.track.p2[1], \
                     self.track.p1[1] + self.track.v1[1], \
                     self.track.p2[1] + self.track.v2[1]]
        return (min(xspan), max(xspan), min(yspan), max(yspan)) 
    
    
    def Scale(self, scale, oMinX, oMaxX, oMinY, oMaxY):
        factor = float(scale / ui.editor.SCALE_FACTOR)
        
        self.curve[0].x = (self.track.p1[0] - oMinX) * factor + 100
        self.curve[0].y = (-self.track.p1[1] - oMinY) * factor + 100
        self.curve[3].x = (self.track.p2[0] - oMinX) * factor + 100
        self.curve[3].y = (-self.track.p2[1] - oMinY) * factor + 100
        
        self.curve[1].x = (self.track.p1[0] + self.track.v1[0] - oMinX) \
            * factor + 100;
        self.curve[1].y = (-self.track.p1[1] - self.track.v1[1] - oMinY) \
            * factor + 100;
        self.curve[2].x = (self.track.p2[0] + self.track.v2[0] - oMinX) \
            * factor + 100;
        self.curve[2].y = (-self.track.p2[1] - self.track.v2[1] - oMinY) \
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
        xspan = [self.switch.p1[0], self.switch.p2[0], \
                     self.switch.p1[0] + self.switch.v1[0], \
                     self.switch.p2[0] + self.switch.v2[0], \
                     self.switch.pc[0], \
                     self.switch.pc[0] + self.switch.vc1[0], \
                     self.switch.pc[0] + self.switch.vc2[0]]
        yspan = [self.switch.p1[1], self.switch.p2[1], \
                     self.switch.p1[1] + self.switch.v1[1], \
                     self.switch.p2[1] + self.switch.v2[1], \
                     self.switch.pc[1], \
                     self.switch.pc[1] + self.switch.vc1[1], \
                     self.switch.pc[1] + self.switch.vc2[1]]
        return (min(xspan), max(xspan), min(yspan), max(yspan))
    
    
    def Scale(self, scale, oMinX, oMaxX, oMinY, oMaxY):
        factor = float(scale / ui.editor.SCALE_FACTOR);
      
        self.straight[0].x = (self.switch.pc[0] - oMinX) * factor + 100;
        self.straight[0].y = (-self.switch.pc[1] - oMinY) * factor + 100;
        self.straight[3].x = (self.switch.p1[0] - oMinX) * factor + 100;
        self.straight[3].y = (-self.switch.p1[1] - oMinY) * factor + 100;
      
        self.straight[1].x = (self.switch.pc[0] + self.switch.vc1[0]-oMinX) \
            * factor + 100;
        self.straight[1].y = (-self.switch.pc[1] - self.switch.vc1[1]-oMinY) \
            * factor + 100;
        self.straight[2].x = (self.switch.p1[0] + self.switch.v1[0]-oMinX) \
            * factor + 100;
        self.straight[2].y = (-self.switch.p1[1] - self.switch.v1[1]-oMinY) \
            * factor + 100;
      
        self.diverging[0].x = (self.switch.pc[0] - oMinX) * factor + 100;
        self.diverging[0].y = (-self.switch.pc[1] - oMinY) * factor + 100;
        self.diverging[3].x = (self.switch.p2[0] - oMinX) * factor + 100;
        self.diverging[3].y = (-self.switch.p2[1] - oMinY) * factor + 100;
      
        self.diverging[1].x = (self.switch.pc[0] + self.switch.vc2[0]-oMinX) \
            * factor + 100;
        self.diverging[1].y = (-self.switch.pc[1] - self.switch.vc2[1]-oMinY) \
            * factor + 100;
        self.diverging[2].x = (self.switch.p2[0] + self.switch.v2[0]-oMinX) \
            * factor + 100;
        self.diverging[2].y = (-self.switch.p2[1] - self.switch.v2[1]-oMinY) \
            * factor + 100;
    
    
    def Draw(self, dc, clip):
        dc.DrawSpline(self.straight)
        dc.DrawSpline(self.diverging)
        
        
    def GetRepaingBounds(self):
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
        return (self.basePoint.point[0], self.basePoint.point[0], \
                self.basePoint.point[1], self.basePoint.point[1])
    
    
    def Scale(self, scale, oMinX, oMaxX, oMinY, oMaxY):
        factor = float(scale / ui.editor.SCALE_FACTOR)
        
        self.point.x = int((self.basePoint.point[0] - oMinX) * factor) + 100
        self.point.y = int((-self.basePoint.point[1] - oMinY) * factor) + 100


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
        
