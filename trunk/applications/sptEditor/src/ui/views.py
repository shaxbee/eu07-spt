"""
Module containing views of scenery elements.

@author adammo
"""

import wx

import model.tracks
import ui.editor


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
        
        Returing tuple has following values (minX, maxX, minZ, maxZ). 
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
        zspan = [self.track.p1[2], self.track.p2[2], \
                     self.track.p1[2] + self.track.v1[2], \
                     self.track.p2[2] + self.track.v2[2]]
        return (min(xspan), max(xspan), min(zspan), max(zspan)) 
    
    
    def Scale(self, scale, oMinX, oMaxX, oMinZ, oMaxZ):
        factor = float(scale / ui.editor.SCALE_FACTOR)
        
        self.curve[0].x = (self.track.p1[0] - oMinX) * factor + 100
        self.curve[0].y = (-self.track.p1[2] - oMinZ) * factor + 100
        self.curve[3].x = (self.track.p2[0] - oMinX) * factor + 100
        self.curve[3].y = (-self.track.p2[2] - oMinZ) * factor + 100
        
        self.curve[1].x = (self.track.p1[0] + self.track.v1[0] - oMinX) \
            * factor + 100;
        self.curve[1].y = (-self.track.p1[2] - self.track.v1[2] - oMinZ) \
            * factor + 100;
        self.curve[2].x = (self.track.p2[0] + self.track.v2[0] - oMinX) \
            * factor + 100;
        self.curve[2].y = (-self.track.p2[2] - self.track.v2[2] - oMinZ) \
            * factor + 100;        
        
    
    def Draw(self, dc, clip):
        dc.DrawSpline(self.curve)


    def GetRepaintBounds(self):
        xspan = [self.curve[0].x, self.curve[1].x, \
                 self.curve[2].x, self.curve[3].x]
        zspan = [self.curve[0].y, self.curve[1].y, \
                 self.curve[2].y, self.curve[3].y]
        l = min(xspan)
        r = max(xspan)
        t = min(zspan)
        b = max(zspan)
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
        zspan = [self.switch.p1[2], self.switch.p2[2], \
                     self.switch.p1[2] + self.switch.v1[2], \
                     self.switch.p2[2] + self.switch.v2[2], \
                     self.switch.pc[2], \
                     self.switch.pc[2] + self.switch.vc1[2], \
                     self.switch.pc[2] + self.switch.vc2[2]]
        return (min(xspan), max(xspan), min(zspan), max(zspan))
    
    
    def Scale(self, scale, oMinX, oMaxX, oMinZ, oMaxZ):
        factor = float(scale / ui.editor.SCALE_FACTOR);
      
        self.straight[0].x = (self.switch.pc[0] - oMinX) * factor + 100;
        self.straight[0].y = (-self.switch.pc[2] - oMinZ) * factor + 100;
        self.straight[3].x = (self.switch.p1[0] - oMinX) * factor + 100;
        self.straight[3].y = (-self.switch.p1[2] - oMinZ) * factor + 100;
      
        self.straight[1].x = (self.switch.pc[0] + self.switch.vc1[0]-oMinX) \
            * factor + 100;
        self.straight[1].y = (-self.switch.pc[2] - self.switch.vc1[2]-oMinZ) \
            * factor + 100;
        self.straight[2].x = (self.switch.p1[0] + self.switch.v1[0]-oMinX) \
            * factor + 100;
        self.straight[2].y = (-self.switch.p1[2] - self.switch.v1[2]-oMinZ) \
            * factor + 100;
      
        self.diverging[0].x = (self.switch.pc[0] - oMinX) * factor + 100;
        self.diverging[0].y = (-self.switch.pc[2] - oMinZ) * factor + 100;
        self.diverging[3].x = (self.switch.p2[0] - oMinX) * factor + 100;
        self.diverging[3].y = (-self.switch.p2[2] - oMinZ) * factor + 100;
      
        self.diverging[1].x = (self.switch.pc[0] + self.switch.vc2[0]-oMinX) \
            * factor + 100;
        self.diverging[1].y = (-self.switch.pc[2] - self.switch.vc2[2]-oMinZ) \
            * factor + 100;
        self.diverging[2].x = (self.switch.p2[0] + self.switch.v2[0]-oMinX) \
            * factor + 100;
        self.diverging[2].y = (-self.switch.p2[2] - self.switch.v2[2]-oMinZ) \
            * factor + 100;
    
    
    def Draw(self, dc, clip):
        dc.DrawSpline(self.straight)
        dc.DrawSpline(self.diverging)
        
        
    def GetRepaingBounds(self):
        xspan = [self.straight[0].x, self.straight[1].x, \
                 self.straight[2].x, self.straight[3].x, \
                 self.diverging[0].x, self.diverging[1].x, \
                 self.diverging[2].x, self.diverging[3].x]
        zspan = [self.straight[0].y, self.straight[1].y, \
                 self.straight[2].y, self.straight[3].y, \
                 self.diverging[0].y, self.diverging[1].y, \
                 self.diverging[2].y, self.diverging[3].y]
        l = min(xspan)
        r = max(xspan)
        t = min(zspan)
        b = max(zspan)
        return wx.Rect(l, t, r-l, b-t)
