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
        
        self.assertEquals(testedPoint,basePoint.point)


 
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
        
        self.assertEquals(testedPoint,basePoint.point)       
        
        
        
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
        
        testedPoint = Vec3(Decimal("187.156"),Decimal("204.205"),Decimal("5.405"))
        testedVec = Vec3(Decimal("-91.973"),Decimal("-33.464"),Decimal("-1.235"))
        self.assertEquals(testedPoint,basePoint.point)
        self.assertEquals(testedVec, track.v2)
        #return angle in degrees in two digits float 
        alfa = math.ceil(math.degrees(math.atan(track.v2[0]/track.v2[1]))*100)/100
        
        
        self.assertEquals(55,alfa)

    def testCreateKrzywaPrzejsciowa(self):
        
        pass

    def testCreateVerticalArc(self):
        
        basePoint = ui.editor.BasePoint()
        
        #basePoint.SetPosition(Vec3(Decimal("-10.293"), Decimal("106.952"), Decimal("0")))
        basePoint.SetPosition(Vec3(Decimal("0"), Decimal("0"), Decimal("0")))
        basePoint.SetAlpha(15)
        basePoint.SetGradient(10)
        
        tf = ui.trackfc.TrackFactory()
        
        track = tf.CreateVerticalArc(22, 2500, basePoint)
        
        testedPoint = Vec3(Decimal("7.761"),Decimal("28.965"),Decimal("0.479"))
        testedVec = Vec3(Decimal("-2.586"),Decimal("-9.654"),Decimal("-0.220"))
        self.assertEquals(testedPoint,basePoint.point)
    

if __name__ == "__main__":
    unittest.main()

