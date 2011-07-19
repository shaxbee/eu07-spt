"""
Test module for ui.views
"""

import unittest
from sptmath import Vec3
from model.tracks import *
from ui.editor import EditorBounds
from ui.views import TrackViewer
import wx


class TrackViewerTest(unittest.TestCase):
    
    def testGetSnapData(self):
        t1 = Track(
            Vec3("-10.293", "106.952", "0"),
            Vec3("-0.565", "4.968", "0"),
            Vec3("0.316", "-4.99", "0"),
            Vec3("-11.715", "121.891", "0"))
        t2 = Track(
            Vec3("-1.924", "33.427", "-1.000"),
            Vec3(),
            Vec3(),
            Vec3("-10.293", "106.952", "0"))
        t1.n1 = t2
        t2.n2 = t1
        
        bounds = EditorBounds()
        bounds.scale = 10.0
        bounds.minX = -55000.0
        bounds.maxX = 1000.0
        bounds.minY = -5000.0
        bounds.maxY = 60000.0
        
        print bounds.ModelToView(Vec3("-10.293", "106.952", "0"))
        
        tv = TrackViewer(t1)
        sd = tv.GetSnapData(bounds, wx.Point(9, 9))
        
        self.assertIsNone(sd)


    
    
if __name__ == "__main__":
    unittest.main()
