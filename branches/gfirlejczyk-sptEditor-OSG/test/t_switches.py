"""
Unit test for rail switches.
"""

import unittest

from sptmath import Vec3
from decimal import Decimal

from model.tracks import *

class SwitchTest(unittest.TestCase):

    def testTrackingConnections(self):
        underTest = Switch( \
            Vec3(Decimal("0.0"), Decimal("0.0"), Decimal("0.0")), \
            Vec3(Decimal("-1.924"), Decimal("33.927"), Decimal("0.0")), \
            Vec3(Decimal("1.924"), Decimal("33.927"), Decimal("0.0")), \
            Vec3(Decimal("0.0"), Decimal("11.336"), Decimal("0.0")), \
            Vec3(Decimal("1.282"), Decimal("-11.263"), Decimal("0.0")), \
            Vec3(Decimal("0.0"), Decimal("11.336"), Decimal("0.0")), \
            Vec3(Decimal("-1.282"), Decimal("-11.263"), Decimal("0.0")))
        t1 = Track( \
            Vec3(Decimal("-1.924"), Decimal("33.427"), Decimal("0.0")), \
            Vec3(Decimal("0.0"), Decimal("0.0"), Decimal("0.0")), \
            Vec3(Decimal("0.0"), Decimal("0.0"), Decimal("0.0")), \
            Vec3(Decimal("-10.292"), Decimal("106.952"), Decimal("0.0")))
        t2 = Track( \
            Vec3(Decimal("0.0"), Decimal("0.0"), Decimal("0.0")), \
            Vec3(Decimal("0.0"), Decimal("0.0"), Decimal("0.0")), \
            Vec3(Decimal("0.0"), Decimal("0.0"), Decimal("0.0")), \
            Vec3(Decimal("0.0"), Decimal("-74.0"), Decimal("0.0")))
        
        underTest.n1 = t1
        underTest.nc = t2
        
        self.assertEquals(Vec3(Decimal("0.0"), Decimal("0.0"), Decimal("0.0")), underTest.tracking2point(t2))
        self.assertEquals(Vec3(Decimal("1.924"), Decimal("33.927"), Decimal("0.0")), \
            underTest.tracking2point(None))
        self.assertEquals(Vec3(Decimal("-1.924"), Decimal("33.927"), Decimal("0.0")), \
            underTest.tracking2point(t1))
        
        self.assertEquals(None, \
            underTest.point2tracking(Vec3(Decimal("1.924"), Decimal("33.927"), Decimal("0.0"))))
        self.assertEquals(t1, \
            underTest.point2tracking(Vec3(Decimal("-1.924"), Decimal("33.927"), Decimal("0.0"))))
        self.assertEquals(t2, \
            underTest.point2tracking(Vec3(Decimal("0.0"), Decimal("0.0"), Decimal("0.0")))) 




if __name__ == '__main__':
    unittest.main()

