"""
Unit tests for track factory module.
"""

import unittest

from sptmath import Vec3, Decimal
from model.tracks import *
import ui.trackfc
import ui.editor
import math

class TrackFactoryTest(unittest.TestCase):

    """
    Wzory:

    Okrag:  
        (x-x0)^2+(y-y0)^2 = r^2
        x = x0 + r*cos(alfa)
        y = y0 + r*sin(alfa)
    
    Bezier: 
        
    Parabola 3stopnia:
        
    """
    
    def testCreateStraight(self):
        
        #editor = ui.editor.SceneryEditor(None,self,0)
        
        basePoint = ui.editor.BasePoint()
        
        #basePoint.SetPosition(Vec3(Decimal("-10.293"), Decimal("106.952"), Decimal("0")))
        basePoint.SetPosition(Vec3())
        basePoint.SetAlpha(55)
        basePoint.SetGradient(22)
        
        tf = ui.trackfc.TrackFactory()
        
        strack = tf.CreateStraight(58.651, basePoint)
        
        testedPoint = Vec3(48.044, 33.641, 1.290)
        
        self.assertEquals(testedPoint,strack.p2)


 
    def testCreateStraightOnStation(self):
        
        #editor = ui.editor.SceneryEditor(None,self,0)
        
        basePoint = ui.editor.BasePoint()
        
        #basePoint.SetPosition(Vec3(Decimal("-10.293"), Decimal("106.952"), Decimal("0")))
        basePoint.SetPosition(Vec3())
        basePoint.SetAlpha(55)
        basePoint.SetGradient(22)
        
        tf = ui.trackfc.TrackFactory()
        
        strack = tf.CreateStraightOnStation(58.651, basePoint)
        testedPoint = Vec3(48.032, 33.633, 1.290)
        
        self.assertEquals(testedPoint,strack.p2)       
        
        
        
    def testCreateArc(self):
        
        basePoint = ui.editor.BasePoint()
        
        basePoint.SetPosition(Vec3())
        basePoint.SetAlpha(15)
        basePoint.SetGradient(22)
        
        tf = ui.trackfc.TrackFactory()
        
        track = tf.CreateHorizontalArc(math.radians(55), 300, False, basePoint)
        
        testedPoint = Vec3(229.813, 192.836, 6.336)
        testedVec = Vec3(-91.977, -33.477, -2.153)
        self.assertEquals(testedPoint,basePoint.point)
        self.assertEquals(testedVec, track.v2)
        #return angle in degrees in two digits float 
        alfa = math.ceil(math.degrees(math.atan(track.v2[0]/track.v2[1]))*100)/100
        
        
        self.assertEquals(70,alfa)



    def testCreateArcOnStation(self):
        
        basePoint = ui.editor.BasePoint()
        
        #basePoint.SetPosition(Vec3(Decimal("-10.293"), Decimal("106.952"), Decimal("0")))
        basePoint.SetPosition(Vec3())
        basePoint.SetAlpha(15)
        basePoint.SetGradient(22)
        
        tf = ui.trackfc.TrackFactory()
        
        track = tf.CreateArcOnStation(math.radians(55), 300, False, basePoint)
        
        testedPoint = Vec3(187.156, 204.205, 5.405)
        testedVec1 = Vec3(25.327, 94.521, 2.153)
        testedVec2 = Vec3(-91.973, -33.464, -1.235)
        self.assertEquals(testedPoint,track.p2)
        self.assertEquals(testedVec1, track.v1)
        self.assertEquals(testedVec2, track.v2)#return angle in degrees in two digits float 
        #alfa = math.ceil(math.degrees(math.atan(track.v2[0]/track.v2[1]))*100)/100
        
        self.assertEquals(70,basePoint.alpha)

    def testCreateKrzywaPrzejsciowa(self):
        
        pass

    def testCreateVerticalArc(self):
        
        basePoint = ui.editor.BasePoint()
        
        #basePoint.SetPosition(Vec3(Decimal("-10.293"), Decimal("106.952"), Decimal("0")))
        basePoint.SetPosition(Vec3())
        basePoint.SetAlpha(15)
        basePoint.SetGradient(10)
        
        tf = ui.trackfc.TrackFactory()
        
        track = tf.CreateVerticalArc(22, 2500, basePoint)
        
        p = 28.966
        #testedPoint2 = Vec3(Decimal(7.761),Decimal(28.966),Decimal(0.479))
        testedPoint2 = Vec3(7.761, 28.966, 0.480)
        testedVec2 = Vec3(-2.587,-9.654,-0.220)
        testedVec1 = Vec3(2.587,9.656,0.100)

        self.assertEquals(testedPoint2,track.p2)
        self.assertEquals(testedVec2,track.v2)
        self.assertEquals(testedVec1,track.v1)

if __name__ == "__main__":
    unittest.main()

