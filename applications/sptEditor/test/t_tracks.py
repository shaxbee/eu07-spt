"""
Unit tests for tracks module.
"""

import unittest

from sptmath import Vec3, Decimal
from model.tracks import *

class TrackTest(unittest.TestCase):

    def testTrackingConnections(self):
        t1 = Track( \
            Vec3(Decimal("-10.293"), Decimal("106.952"), Decimal("0")), \
            Vec3(Decimal("-0.565"), Decimal("4.968"), Decimal("0")), \
            Vec3(Decimal("0.316"), Decimal("-4.99"), Decimal("0")), \
            Vec3(Decimal("-11.715"), Decimal("121.891"), Decimal("0")))
        r2 = Switch( \
            pc = Vec3(Decimal("0"), Decimal("0"), Decimal("0")), \
            p1 = Vec3(Decimal("-1.924"), Decimal("33.927"), Decimal("0")), \
            p2 = Vec3(Decimal("1.924"), Decimal("33.927"), Decimal("0")), \
            vc1 = Vec3(Decimal("0"), Decimal("11.336"), Decimal("0")), \
            vc2 = Vec3(Decimal("0"), Decimal("11.336"), Decimal("0")), \
            v1 = Vec3(Decimal("1.282"), Decimal("-11.263"), Decimal("0")), \
            v2 = Vec3(Decimal("-1.282"), Decimal("-11.263"), Decimal("0")))
        underTest = Track( \
            Vec3(Decimal("-1.924"), Decimal("33.427"), Decimal("0")), \
            Vec3(), \
            Vec3(), \
            Vec3(Decimal("-10.292"), Decimal("106.952"), Decimal("0")))

        underTest.n1 = r2
        underTest.n2 = t1

        self.assertEquals(Vec3(Decimal("-1.924"), Decimal("33.427"), Decimal("0")), \
            underTest.tracking2point(r2))
        self.assertEquals(Vec3(Decimal("-1.924"), Decimal("33.427"), Decimal("0")), \
            underTest.tracking2point(r2))

        self.assertEquals(t1, underTest.point2tracking( \
            Vec3(Decimal("-10.292"), Decimal("106.952"), Decimal("0"))))
        self.assertEquals(r2, underTest.point2tracking( \
            Vec3(Decimal("-1.924"), Decimal("33.427"), Decimal("0"))))


    def testTrackingConnectionsNull(self):
        r2 = Switch( \
            pc = Vec3(), \
            p1 = Vec3(Decimal("-1.924"), Decimal("33.927"), Decimal("0")), \
            p2 = Vec3(Decimal("1.924"), Decimal("33.927"), Decimal("0")), \
            vc1 = Vec3(Decimal("0.0"), Decimal("11.336"), Decimal("0")), \
            v1 = Vec3(Decimal("1.282"), Decimal("-11.263"), Decimal("0")), \
            vc2 = Vec3(Decimal("0.0"), Decimal("11.336"), Decimal("0")), \
            v2 = Vec3(Decimal("-1.282"), Decimal("-11.263"), Decimal("0")))
        underTest = Track( \
            Vec3(Decimal("-1.924"), Decimal("33.427"), Decimal("0")), \
            Vec3(), \
            Vec3(), \
            Vec3(Decimal("-10.292"), Decimal("106.952"), Decimal("0")))
    
        underTest.n1 = r2
    
        self.assertEquals(Vec3(Decimal("-1.924"), Decimal("33.427"), Decimal("0")), \
            underTest.tracking2point(r2))
        self.assertEquals(Vec3(Decimal("-10.292"), Decimal("106.952"), Decimal("0")), \
            underTest.tracking2point(None))
    
        self.assertEquals(None, \
            underTest.point2tracking(Vec3(Decimal("-10.292"), Decimal("106.952"), Decimal("0"))))
        self.assertEquals(r2, \
            underTest.point2tracking(Vec3(Decimal("-1.924"), Decimal("33.427"), Decimal("0"))))




if __name__ == "__main__":
    unittest.main()

