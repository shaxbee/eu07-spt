"""
Module containg various classes and functions that operates
on tracks within editor.

@author Adammo
"""

from math import sin, cos
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
        v1 = Vec3()
        v2 = Vec3()
        p1 = Vec3()

        basePoint = self.editor.basePoint
        opoint = basePoint.point

        tr = BasePointTransform(basePoint.point, basePoint.alpha)
        tr.Transform(p1, v1, v2, p2)

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


    def Transform(self, p1, v1, v2, p2):
        pass




class BasePointTransform(AbstractTransform):
    """
    Moves and rotates the geometry of track according base point.
    """

    def __init__(self, point, alpha):
        AbstractTransform.__init__(self)
        self.point = point
        self.alpha = alpha


    def Transform(self, p1, v1, v2, p2):
        sin_a = sin(self.alpha)
        cos_a = cos(self.alpha)

        matrix = [ \
            [cos_a, 0.0, sin_a, self.point.x], \
            [0.0, 1.0, 0.0, self.point.y], \
            [-sin_a, 0.0, cos_a, self.point.z], \
            [0.0, 0.0, 0.0, 1.0]]

        transformVec3(matrix, p1)
        transformVec3(matrix, v1)
        transformVec3(matrix, v2)
        transformVec3(matrix, p2)




def transformVec3(m, vec3):
    """
    Transforms Vec3 using matrix 4x4
    """
    x, y, z = float(vec3.x), float(vec3.y), float(vec3.z)

    # Last column is just a decimal - no loss of precision
    vec3.x = decimal.Decimal(str(m[0][0] * x + m[0][1] * y + m[0][2] * z)) + m[0][3]
    vec3.y = decimal.Decimal(str(m[1][0] * x + m[1][1] * y + m[1][2] * z)) + m[1][3]
    vec3.z = decimal.Decimal(str(m[2][0] * x + m[2][1] * y + m[2][2] * z)) + m[2][3]


