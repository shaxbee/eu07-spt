"""
Module containg various classes and functions that operates
on tracks within editor.

@author Adammo
"""

from math import sin, cos, atan, radians
import decimal

from sptmath import Vec3
from model.tracks import Track


class TrackFactory:
    """
    Factory methods for tracks.
    """

    def __init__(self, editor):
        self.editor = editor


    def CreateStraight(self, length):
        p2 = Vec3("0", str(length), "0")
        p1 = Vec3()

        basePoint = self.editor.basePoint
        opoint = basePoint.point

        tr = BasePointTransform(basePoint)
        tr.Transform([p1, p2])

        v1 = Vec3()
        v2 = Vec3()

        npoint = Vec3()
        npoint.x = p2.x
        npoint.y = p2.y
        npoint.z = p2.z
        basePoint.point = npoint

        # Refresh editor
        self.editor.SetBasePoint(basePoint)

        return Track(p1, v1, v2, p2)




class AbstractTransform:
    """
    A transform does something with the geometry of track.
    """
    
    def __init__(self):
        pass


    def Transform(self, vectors):
        pass




class BasePointTransform(AbstractTransform):
    """
    Moves and rotates the geometry of track according base point.
    """

    def __init__(self, basePoint):
        AbstractTransform.__init__(self)
        self.point = basePoint.point
        self.alpha = -radians(basePoint.alpha)
        self.beta = atan(basePoint.gradient / 1000.0)


    def Transform(self, vectors):
        sin_a = sin(self.alpha)
        cos_a = cos(self.alpha)
        sin_b = sin(self.beta)
        cos_b = cos(self.beta)

        # Matrices for 3D transformations 
        matrix = [ \
            [cos_a, -sin_a, 0.0, self.point.x], \
            [cos_b*sin_a, cos_a*cos_b, -sin_b, self.point.y], \
            [sin_a*sin_b, sin_b*cos_a, cos_b, self.point.z], \
            [0.0, 0.0, 0.0, 1.0]]

        for v in vectors:
            transformVec3(matrix, v)




def transformVec3(m, vec3):
    """
    Transforms Vec3 using matrix 4x4
    """
    x, y, z = float(vec3.x), float(vec3.y), float(vec3.z)

    # Last column is just a decimal - no loss of precision
    vec3.x = decimal.Decimal(str(m[0][0] * x + m[0][1] * y + m[0][2] * z)) + m[0][3]
    vec3.y = decimal.Decimal(str(m[1][0] * x + m[1][1] * y + m[1][2] * z)) + m[1][3]
    vec3.z = decimal.Decimal(str(m[2][0] * x + m[2][1] * y + m[2][2] * z)) + m[2][3]


