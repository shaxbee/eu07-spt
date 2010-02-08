"""
Test module containing test cases for RailGroup.

@author Adammo
"""

import unittest
import logging.config
import sys
import os.path

from sptmath import Vec3
from model.groups import RailGroup
from model.tracks import *


class RailContainerTest(unittest.TestCase):

    def testSingle(self):
        railSwitch = Switch( \
            pc = Vec3("0.0", "0.0", "0.0"), \
            p1 = Vec3("0.0", "33.23", "0.0"), \
            p2 = Vec3("-1.837", "33.162", "0.0"), \
            vc1 = Vec3("0.0", "0.0", "0.0"), \
            v1 = Vec3("0.0", "0.0", "0.0"), \
            vc2 = Vec3("0.0", "11.079", "0.0"), \
            v2 = Vec3("-0.776", "-6.974", "0.0"))
    
        group = RailGroup()
    
        group.insert(railSwitch)
    
        self.assertEquals(1, group.size())
    
        endpoints = group.connections.keys()
        self.assertTrue(Vec3("0", "0", "0") in endpoints)
        self.assertTrue(Vec3("0.0", "33.23", "0") in endpoints)
        self.assertTrue(Vec3("-1.837", "33.162", "0") in endpoints)
        self.assertEquals(3, len(endpoints))


    def testUnconnected(self):
        t1 = Track( \
            Vec3("0.0", "0.0", "0.0"), \
            Vec3("0.0", "0.0", "0.0"), \
            Vec3("0.0", "0.0", "0.0"), \
            Vec3("0.0", "100.0", "0.0"))
        t2 = Track( \
            Vec3("5.0", "0.0", "0.0"), \
            Vec3("0.0", "0.0", "0.0"), \
            Vec3("0.0", "0.0", "0.0"), \
            Vec3("5.0", "100.0", "0.0"))
    
        group = RailGroup()
    
        group.insert(t1)
        group.insert(t2)
    
        self.assertEquals(2, group.size())
    
        endpoints = group.connections.keys()
        self.assertTrue(Vec3("0.0", "0.0", "0.0") in endpoints)
        self.assertTrue(Vec3("5.0", "0.0", "0.0") in endpoints)
        self.assertTrue(Vec3("5.0", "100.0", "0.0") in endpoints)
        self.assertTrue(Vec3("0.0", "100.0", "0.0") in endpoints)
        self.assertEquals(4, len(endpoints))


    def testDoubleSlip(self):
        a = Switch( \
            pc = Vec3("0.0", "0.0", "0.0"), \
            p1 = Vec3("0.0", "10.423", "0.0"), \
            p2 = Vec3("0.285", "10.418", "0.0"), \
            vc1 = Vec3("0.0", "0.0", "0.0"), \
            v1 = Vec3("0.0", "0.0", "0.0"), \
            vc2 = Vec3("0.0", "3.476", "0.0"), \
            v2 = Vec3("-0.19", "-3.469", "0.0"))
        b = Switch( \
            pc = Vec3("0.0", "20.846", "0.0"), \
            p1 = Vec3("0.0", "10.423", "0.0"), \
            p2 = Vec3("-0.286", "10.428", "0.0"), \
            vc1 = Vec3("0.0", "0.0", "0.0"), \
            v1 = Vec3("0.0", "0.0", "0.0"), \
            vc2 = Vec3("0.0", "-3.476", "0.0"), \
            v2 = Vec3("0.19", "3.469", "0.0"))
        c = Switch( \
            pc = Vec3("-1.142", "0.042", "0.0"), \
            p1 = Vec3("-0.001", "10.442", "0.0"), \
            p2 = Vec3("-0.286", "10.428", "0.0"), \
            vc1 = Vec3("0", "0", "0"), \
            v1 = Vec3("0", "0", "0"), \
            vc2 = Vec3("0.38", "3.454", "0.0"), \
            v2 = Vec3("-0.189", "-3.468", "0.0"))
        d = Switch( \
            pc = Vec3("1.141", "20.803", "0.0"), \
            p1 = Vec3("-0.001", "10.442", "0.0"), \
            p2 = Vec3("0.285", "10.418", "0.0"),  \
            vc1 = Vec3("0", "0", "0"), \
            v1 = Vec3("0", "0", "0"), \
            vc2 = Vec3("-0.38", "-3.454", "0"), \
            v2 = Vec3("0.189", "3.468", "0.0"))
 
        group = RailGroup()
     
        group.insert(a)
        group.insert(b)
        group.insert(c)
        group.insert(d)
     
        self.assertEquals(4, group.size())
    
        endpoints = group.connections.keys()
        self.assertTrue(Vec3("0", "0", "0") in endpoints)
        self.assertTrue(Vec3("0.0", "20.846", "0.0") in endpoints)
        self.assertTrue(Vec3("-1.142", "0.042", "0.0") in endpoints)
        self.assertTrue(Vec3("1.141", "20.803", "0.0") in endpoints)
        self.assertEquals(4, len(endpoints))


    def testCrossing(self):
        v1 = Track( \
            Vec3("0", "0", "0"), \
            Vec3("0", "0", "0"), \
            Vec3("0", "0", "0"), \
            Vec3("-10", "-10", "0"))
        v2 = Track( \
            Vec3("10", "10", "0"), \
            Vec3("0", "0", "0"), \
            Vec3("0", "0", "0"), \
            Vec3("0", "0", "0"))
        h1 = Track( \
            Vec3("0", "0", "0"), \
            Vec3("0", "0", "0"), \
            Vec3("0", "0", "0"), \
            Vec3("-10", "10", "0"))
        h2 =  Track( \
            Vec3("10", "-10", "0"), \
            Vec3("0", "0", "0"), \
            Vec3("0", "0", "0"), \
            Vec3("0", "0", "0"))
    
        group = RailGroup()
    
        group.insert(v1)
        group.insert(v2)
        group.insert(h1)
        group.insert(h2)
    
        self.assertEquals(4, group.size())
    
        endpoints = group.connections.keys()
        self.assertTrue(Vec3("10", "10", "0") in endpoints)
        self.assertTrue(Vec3("10", "-10", "0") in endpoints)
        self.assertTrue(Vec3("-10", "10", "0") in endpoints)
        self.assertTrue(Vec3("-10", "-10", "0") in endpoints)
        self.assertEquals(4, len(endpoints))
  
  
    def testSingleSlip(self):
        t1 = Track( \
            Vec3("0", "20.846", "0"), \
            Vec3("0", "0", "0"), \
            Vec3("0", "0", "0"), \
            Vec3("0", "10.423", "0"))
        t2 =  Track( \
            Vec3("0", "10.424", "0"), \
            Vec3("0", "0", "0"), \
            Vec3("0", "0", "0"), \
            Vec3("-1.141", "0.082", "0"))
        a = Switch( \
            pc = Vec3("0.0", "0.0", "0.0"), \
            p1 = Vec3("0.0", "10.423", "0.0"), \
            p2 = Vec3("0.285", "10.418", "0.0"), \
            vc1 = Vec3("0.0", "0.0", "0.0"), \
            v1 = Vec3("0.0", "0.0", "0.0"), \
            vc2 = Vec3("0.0", "3.476", "0.0"), \
            v2 = Vec3("-0.19", "-3.469", "0.0"))
        b = Switch( \
            pc = Vec3("1.141", "20.803", "0"), \
            p1 = Vec3("0.0", "10.424", "0"), \
            p2 = Vec3("0.285", "10.418", "0"), \
            vc1 = Vec3("0.0", "0.0", "0.0"), \
            v1 = Vec3("0.0", "0.0", "0.0"), \
            vc2 = Vec3("0.0", "-3.476", "0"), \
            v2 = Vec3("0.19", "3.469", "0"))

        group = RailGroup()
    
        group.insert(t1)
        group.insert(t2)
        group.insert(a)
        group.insert(b)
    
        self.assertEquals(4, group.size())
    
        endpoints = group.connections.keys()
        self.assertTrue(Vec3("0", "0", "0") in endpoints)
        self.assertTrue(Vec3("0.0", "20.846", "0") in endpoints)
        self.assertTrue(Vec3("-1.141", "0.082", "0") in endpoints)
        self.assertTrue(Vec3("1.141", "20.803", "0") in endpoints)
        self.assertEquals(4, len(endpoints))

  
    def testEquality(self):
        t1 = Track( \
            Vec3("0", "0", "0"), \
            Vec3("0", "0", "0"), \
            Vec3("0", "0", "0"), \
            Vec3("0", "10.423", "0"))
        t2 =  Track( \
            Vec3("0", "10.423", "0"), \
            Vec3("0", "0", "0"), \
            Vec3("0", "0", "0"), \
            Vec3("-1.141", "0.082", "0"))

        group1 = RailGroup()
        group2 = RailGroup()
    
        group1.insert(t1)
        group1.insert(t2)
        group2.insert(t2)
        group2.insert(t1)
    
        self.assertTrue(group1 == group2)

  
#    def testHashCode(self):
#        t1 = Track( \
#            Vec3("0", "0", "0"), \
#            Vec3("0", "0", "0"), \
#            Vec3("0", "0", "0"), \
#            Vec3("0", "10.423", "0"))
#        t2 = Track( \
#            Vec3("0", "10.423", "0"), \
#            Vec3("0", "0", "0"), \
#            Vec3("0", "0", "0"), \
#            Vec3("-1.141", "0.082", "0"))
#
#        group1 = RailGroup()
#        group2 = RailGroup()
#    
#        group1.insert(t1)
#        group1.insert(t2)
#        group2.insert(t2)
#        group2.insert(t1)
#    
#        self.assertEquals(hash(group1), hash(group2))
 
 
    def testInsertRemove(self):
        #track { -2.501 39.124 0.0  0.0 0.0 0.0  0.0 0.0 0.0  -1.838 33.162 0.0 }
        t1 = Track(Vec3("-2.501", "39.124", "0"), \
            Vec3("0", "0", "0"), \
            Vec3("0", "0", "0"), \
            Vec3("-1.838", "33.162", "0"))
        #track { -3.673 62.125 0.0  0.0 0.0 0.0  0.0 0.0 0.0  -3.673 60.126 0.0 }
        t2 = Track( \
            Vec3("-3.673", "62.125" "0"), \
            Vec3("0", "0", "0"), \
            Vec3("0", "0", "0"), \
            Vec3("-3.673", "60.126", "0"))
        #track { -7.976 -16.881 0.0  -0.187 16.665 0.0  0.881 -16.644 0.0  -9.58 33.09 0.0 }
        t3 = Track( \
            Vec3("-7.976", "-16.881", "0"), \
            Vec3("-0.187", "16.665", "0"), \
            Vec3("0.881", "-16.644" "0"), \
            Vec3("-9.58", "33.09", "0"))
    
        # switch { 0.0 0.0 0.0  0.0 0.0 0.0  0.0 0.0 0.0  0.0 33.23 0.0  0.0 0.0 0.0  0.0 11.079 0.0  1.225 -11.012 0.0  -1.838 33.162 0.0 }
        r1 = Switch( \
            pc = Vec3("0", "0", "0"), \
            p1 = Vec3("0.0", "33.23", "0"), \
            p2 = Vec3("-1.838", "33.162", "0"), \
            vc1 = Vec3("0", "0", "0"), \
            v1 = Vec3("0", "0", "0"), \
            vc2 = Vec3("0.0", "11.079", "0"), \
            v2 = Vec3("1.225", "-11.012", "0"))
        #switch { -3.673 60.126 0.0  0.0 0.0 0.0  0.0 0.0 0.0  -3.662 32.989 0.0  -3.673 60.126 0.0  0.0020 -7.016 0.0  -0.777 6.973 0.0  -2.501 39.124 0.0 }
        r2 = Switch( \
            pc = Vec3("-3.673", "60.126", "0"), \
            p1 = Vec3("-3.662", "32.989", "0"), \
            p2 = Vec3("-2.501", "39.124", "0"), \
            vc1 = Vec3("0", "0", "0"), \
            v1 = Vec3("0", "0", "0"), \
            vc2 = Vec3("0.002", "-7.016", "0"), \
            v2 = Vec3("-0.777", "6.973", "0"))
        #switch { -7.602 -50.108 0.0  0.0 0.0 0.0  0.0 0.0 0.0  -7.976 -16.881 0.0  -7.602 -50.108 0.0  -0.124 11.078 0.0  -1.1 -11.024 0.0  -6.138 -16.929 0.0 }
        r3 = Switch( \
            pc = Vec3("-7.602", "-50.108", "0"), \
            p1 = Vec3("-7.976", "-16.881", "0"), \
            p2 = Vec3("-6.138", "-16.929", "0"), \
            vc1 = Vec3("0", "0", "0"), \
            v1 = Vec3("0", "0", "0"), \
            vc2 = Vec3("-0.124", "11.078", "0"), \
            v2 = Vec3("-1.1", "-11.024", "0"))

        group =  RailGroup()
    
        group.insert(t1);    
        outline = group.connections.keys()
        self.assertEquals(2, len(outline))
        self.assertTrue(Vec3("-2.501", "39.124", "0") in outline)
        self.assertTrue(Vec3("-1.838", "33.162", "0") in outline)    
    
        group.insert(r1)
        outline = group.connections.keys()
        self.assertEquals(3, len(outline))
        self.assertTrue(Vec3("-2.501", "39.124", "0") in outline)
        self.assertTrue(Vec3("0", "0", "0") in outline)
        self.assertTrue(Vec3("0", "33.23", "0") in outline)
    
        group.insert(r2)
        outline = group.connections.keys()
        self.assertEquals(4, len(outline))
        self.assertTrue(Vec3("0", "0", "0") in outline)
        self.assertTrue(Vec3("0", "33.23", "0") in outline)
        self.assertTrue(Vec3("-3.673", "60.126", "0") in outline)
        self.assertTrue(Vec3("-3.662", "32.989", "0") in outline)
    
        group.insert(t2)
        outline = group.connections.keys()
        self.assertEquals(4, len(outline))
        self.assertTrue(Vec3("0", "0", "0") in outline)
        self.assertTrue(Vec3("0", "33.23", "0") in outline)    
        self.assertTrue(Vec3("-3.662", "32.989", "0") in outline)
        self.assertTrue(Vec3("-3.673", "62.125") in outline)
    
        group.insert(r3)
        outline = group.connections.keys()
        self.assertEquals(7, len(outline))
        self.assertTrue(Vec3("0", "0", "0") in outline)
        self.assertTrue(Vec3("0", "33.23", "0") in outline)    
        self.assertTrue(Vec3("-3.662", "32.989", "0") in outline)
        self.assertTrue(Vec3("-3.673", "62.125", "0") in outline)
        self.assertTrue(Vec3("-7.602", "-50.108", "0") in outline)
        self.assertTrue(Vec3("-7.976", "-16.881", "0") in outline)
        self.assertTrue(Vec3("-6.138", "-16.929", "0") in outline)
    
        group.insert(t3)
        outline = group.connections.keys()
        self.assertEquals(7, len(outline))
        self.assertTrue(Vec3("0", "0", "0") in outline)
        self.assertTrue(Vec3("0", "33.23", "0") in outline)    
        self.assertTrue(Vec3("-3.662", "32.989", "0") in outline)
        self.assertTrue(Vec3("-3.673", "62.125", "0") in outline)
        self.assertTrue(Vec3("-7.602", "-50.108", "0") in outline)
        self.assertTrue(Vec3("-6.138", "-16.929", "0") in outline)
        self.assertTrue(Vec3("-9.58", "33.09", "0") in outline)
    
        group.remove(t2)
        outline = group.connections.keys()
        self.assertEquals(7, len(outline))
        self.assertTrue(Vec3("0", "0", "0") in outline)
        self.assertTrue(Vec3("0", "33.23", "0") in outline)
        self.assertTrue(Vec3("-3.662", "32.989", "0") in outline)
        self.assertTrue(Vec3("-3.673", "60.126", "0") in outline)
        self.assertTrue(Vec3("-7.602", "-50.108", "0") in outline)
        self.assertTrue(Vec3("-6.138", "-16.929", "0") in outline)
        self.assertTrue(Vec3("-9.58", "33.09", "0") in outline)
  
  
    def testContains(self):
        #track { -2.501 39.124 0.0  0.0 0.0 0.0  0.0 0.0 0.0  -1.838 33.162 0.0 }
        t1 = Track(Vec3("-2.501", "39.124", "0.0"), Vec3("0", "0", "0"), Vec3("0", "0", "0"), \
            Vec3("-1.838", "33.162", "0"))
        #track { -3.673 62.125 0.0  0.0 0.0 0.0  0.0 0.0 0.0  -3.673 60.126 0.0 }
        t2 = Track(Vec3("-3.673", "62.125", "0"), Vec3("0", "0", "0"), Vec3("0", "0", "0"), \
            Vec3("-3.673", "60.126", "0"))
        #track { -7.976 -16.881 0.0  -0.187 16.665 0.0  0.881 -16.644 0.0  -9.58 33.09 0.0 }
        t3 = Track(Vec3("-7.976", "-16.881", "0"), Vec3("-0.187", "16.665", "0"), \
            Vec3("0.881", "-16.644", "0"), Vec3("-9.58", "33.09", "0"))
    
        # switch { 0.0 0.0 0.0  0.0 0.0 0.0  0.0 0.0 0.0  0.0 33.23 0.0  0.0 0.0 0.0  0.0 11.079 0.0  1.225 -11.012 0.0  -1.838 33.162 0.0 }
        r1 = Switch(Vec3("0", "0", "0"), Vec3("0.0", "33.23", "0"), Vec3("-1.838", "33.162", "0"), \
            Vec3("0", "0", "0"), Vec3("0", "0", "0"), Vec3("0.0", "11.079", "0"), Vec3("1.225", "-11.012", "0"))
        #switch { -3.673 60.126 0.0  0.0 0.0 0.0  0.0 0.0 0.0  -3.662 32.989 0.0  -3.673 60.126 0.0  0.0020 -7.016 0.0  -0.777 6.973 0.0  -2.501 39.124 0.0 }
        r2 = Switch(Vec3("-3.673", "60.126", "0"), Vec3("-3.662", "32.989", "0"), Vec3("-2.501", "39.124", "0"), \
            Vec3("0", "0", "0"), Vec3("0", "0", "0"), Vec3("0.0020", "-7.016", "0"), Vec3("-0.777", "6.973", "0"))
        #switch { -7.602 -50.108 0.0  0.0 0.0 0.0  0.0 0.0 0.0  -7.976 -16.881 0.0  -7.602 -50.108 0.0  -0.124 11.078 0.0  -1.1 -11.024 0.0  -6.138 -16.929 0.0 }
        r3 = Switch(Vec3("-7.602", "-50.108", "0"), Vec3("-7.976", "-16.881", "0"), \
            Vec3("-6.138", "-16.929", "0"), \
            Vec3("0", "0", "0"), Vec3("0", "0", "0"), Vec3("-0.124", "11.078", "0"), Vec3("-1.1", "-11.024", "0"))

        group =  RailGroup()
    
        group.insert(t1)
        self.assertTrue(group.containsPoint(Vec3("-2.501", "39.124", "0")))
        self.assertTrue(group.containsPoint(Vec3("-1.838", "33.162", "0")))    
    
        group.insert(r1)
        self.assertTrue(group.containsPoint( Vec3("-2.501", "39.124", "0")))
        self.assertTrue(group.containsPoint( Vec3("0", "0", "0")))
        self.assertTrue(group.containsPoint( Vec3("0", "33.23", "0")))
    
        group.insert(r2)
        self.assertTrue(group.containsPoint( Vec3("0", "0", "0")))
        self.assertTrue(group.containsPoint( Vec3("0", "33.23", "0")))
        self.assertTrue(group.containsPoint( Vec3("-3.673", "60.126", "0")))
        self.assertTrue(group.containsPoint( Vec3("-3.662", "32.989", "0")))
    
        group.insert(t2)
        self.assertTrue(group.containsPoint( Vec3("0", "0", "0")))
        self.assertTrue(group.containsPoint( Vec3("0", "33.23", "0")))
        self.assertTrue(group.containsPoint( Vec3("-3.662", "32.989", "0")))
        self.assertTrue(group.containsPoint( Vec3("-3.673", "62.125", "0")))
    
        group.insert(r3)
        self.assertTrue(group.containsPoint( Vec3("0", "0", "0")))
        self.assertTrue(group.containsPoint( Vec3("0", "33.23", "0")))
        self.assertTrue(group.containsPoint( Vec3("-3.662", "32.989", "0")))
        self.assertTrue(group.containsPoint( Vec3("-3.673", "62.125", "0")))
        self.assertTrue(group.containsPoint( Vec3("-7.602", "-50.108", "0")))
        self.assertTrue(group.containsPoint( Vec3("-7.976", "-16.881", "0")))
        self.assertTrue(group.containsPoint( Vec3("-6.138", "-16.929", "0")))
    
        group.insert(t3)
        self.assertTrue(group.containsPoint( Vec3("0", "0", "0")))
        self.assertTrue(group.containsPoint( Vec3("0", "33.23", "0")))
        self.assertTrue(group.containsPoint( Vec3("-3.662", "32.989", "0")))
        self.assertTrue(group.containsPoint( Vec3("-3.673", "62.125", "0")))
        self.assertTrue(group.containsPoint( Vec3("-7.602", "-50.108", "0")))
        self.assertTrue(group.containsPoint( Vec3("-6.138", "-16.929", "0")))
        self.assertTrue(group.containsPoint( Vec3("-9.58", "33.09", "0")))
    
        group.remove(t2)
        self.assertTrue(group.containsPoint( Vec3("0", "0", "0")))
        self.assertTrue(group.containsPoint( Vec3("0", "33.23", "0")))
        self.assertTrue(group.containsPoint( Vec3("-3.662", "32.989", "0")))
        self.assertTrue(group.containsPoint( Vec3("-3.673", "60.126", "0")))
        self.assertTrue(group.containsPoint( Vec3("-7.602", "-50.108", "0")))
        self.assertTrue(group.containsPoint( Vec3("-6.138", "-16.929", "0")))
        self.assertTrue(group.containsPoint( Vec3("-9.58", "33.09", "0")))




if __name__ == "__main__":
     # Optionally specify logging configuration by an argument in command line
     # and apply it
     if sys.argv[1] != None and os.path.isfile(sys.argv[1]):
         logging.config.fileConfig(sys.argv[1])
     unittest.main(argv = [sys.argv[0]])

