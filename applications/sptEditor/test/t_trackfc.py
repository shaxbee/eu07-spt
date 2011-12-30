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
        basePoint.SetPosition(Vec3(Decimal("0"), Decimal("0"), Decimal("0")))
        basePoint.SetAlpha(55)
        basePoint.SetGradient(22)
        
        tf = ui.trackfc.TrackFactory()
        
        strack = tf.CreateStraight(58.651, basePoint)
        
        testedPoint = Vec3(Decimal("48.044"),Decimal("33.641"),Decimal("1.290"))
        
        self.assertEquals(testedPoint,strack.p2)


 
    def testCreateStraightOnStation(self):
        
        #editor = ui.editor.SceneryEditor(None,self,0)
        
        basePoint = ui.editor.BasePoint()
        
        #basePoint.SetPosition(Vec3(Decimal("-10.293"), Decimal("106.952"), Decimal("0")))
        basePoint.SetPosition(Vec3(Decimal("0"), Decimal("0"), Decimal("0")))
        basePoint.SetAlpha(55)
        basePoint.SetGradient(22)
        
        tf = ui.trackfc.TrackFactory()
        
        strack = tf.CreateStraightOnStation(58.651, basePoint)
        
        testedPoint = Vec3(Decimal("48.032"),Decimal("33.632"),Decimal("1.290"))
        
        self.assertEquals(testedPoint,strack.p2)       
        
        
        
    def testCreateArc(self):
        
        basePoint = ui.editor.BasePoint()
        
        #basePoint.SetPosition(Vec3(Decimal("-10.293"), Decimal("106.952"), Decimal("0")))
        basePoint.SetPosition(Vec3(Decimal("0"), Decimal("0"), Decimal("0")))
        basePoint.SetAlpha(15)
        basePoint.SetGradient(22)
        
        tf = ui.trackfc.TrackFactory()
        
        track = tf.CreateHorizontalArc(math.radians(55), 300, False, basePoint)
        
        testedPoint = Vec3(Decimal("187.172"),Decimal("204.262"),Decimal("6.336"))
        testedVec = Vec3(Decimal("-91.977"),Decimal("-33.477"),Decimal("-2.153"))
        self.assertEquals(testedPoint,basePoint.point)
        self.assertEquals(testedVec, track.v2)
        #return angle in degrees in two digits float 
        alfa = math.ceil(math.degrees(math.atan(track.v2[0]/track.v2[1]))*100)/100
        
        
        self.assertEquals(55,alfa)



    def testCreateArcOnStation(self):
        
        basePoint = ui.editor.BasePoint()
        
        #basePoint.SetPosition(Vec3(Decimal("-10.293"), Decimal("106.952"), Decimal("0")))
        basePoint.SetPosition(Vec3(Decimal("0"), Decimal("0"), Decimal("0")))
        basePoint.SetAlpha(15)
        basePoint.SetGradient(22)
        
        tf = ui.trackfc.TrackFactory()
        
        track = tf.CreateArcOnStation(math.radians(55), 300, False, basePoint)
        
        testedPoint = Vec3(Decimal("187.156"),Decimal("204.204"),Decimal("5.405"))
        testedVec1 = Vec3(Decimal("25.326"),Decimal("94.521"),Decimal("2.152"))
        testedVec2 = Vec3(Decimal("-91.973"),Decimal("-33.463"),Decimal("-1.234"))
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
        basePoint.SetPosition(Vec3(0,0,0))
        basePoint.SetAlpha(15)
        basePoint.SetGradient(10)
        
        tf = ui.trackfc.TrackFactory()
        
        track = tf.CreateVerticalArc(22, 2500, basePoint)
        
        testedPoint2 = Vec3(Decimal(7.7611),Decimal(28.9661),Decimal(0.4791))
        testedVec2 = Vec3(Decimal(-2.5861),Decimal(-9.6541),Decimal(-0.2191))
        testedVec1 = Vec3(Decimal(2.5871),Decimal(9.6561),Decimal(0.0991))
        self.assertEquals(testedPoint2,track.p2)
        self.assertEquals(testedVec2,track.v2)
        self.assertEquals(testedVec1,track.v1)

if __name__ == "__main__":
    unittest.main()

