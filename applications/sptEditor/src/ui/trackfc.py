"""
Module containg various classes and functions that operates
on tracks within editor.

@author Adammo
"""

from math import sin, cos, atan, radians, pi, degrees
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

        tr = BasePointTransform(basePoint)
        tr.Transform([p1, p2], [])

        v1 = Vec3()
        v2 = Vec3()

        basePoint.point = Vec3(p2.x, p2.y, p2.z)

        # Refresh editor
        self.editor.SetBasePoint(basePoint)

        return Track(p1, v1, v2, p2)


    def CreateCurve(self, length, radius, isLeft):
        """
        Creates curve track
        """
        angle = length / radius
        half = 0.5 * angle
        sin_a = sin(half)
        cos_a = cos(half)

        p1 = Vec3()
        p2 = Vec3()
        v1 = Vec3()
        v2 = Vec3()

        p1.x = decimal.Decimal(str(-radius * cos_a))
        p1.y = decimal.Decimal(str(radius * sin_a))
        p2.x = decimal.Decimal(str(-radius * cos_a))
        p2.y = decimal.Decimal(str(-radius * sin_a))

        ctrlX = -radius * (4.0 - cos_a) / 3.0
        ctrlY = -radius * (1.0 - cos_a) * (cos_a - 3.0) / (3.0 * sin_a)

        v1.x = decimal.Decimal(str(ctrlX)) - p1.x
        v1.y = decimal.Decimal(str(ctrlY)) - p1.y
        v2.x = decimal.Decimal(str(ctrlX)) - p2.x
        v2.y = decimal.Decimal(str(-ctrlY)) - p2.y

        # Left or right
        tr = LeftTrackTransform(length, radius) if isLeft \
            else RightTrackTransform(length, radius)
        tr.Transform([p1, p2], [v1, v2])

        basePoint = self.editor.basePoint

        tr = BasePointTransform(basePoint)
        tr.Transform([p1, p2], [v1, v2])
        
        basePoint.point = Vec3(p2.x, p2.y, p2.z)
        if isLeft:
            basePoint.alpha -= degrees(angle)
        else:
            basePoint.alpha += degrees(angle)

        # Refresh editor
        self.editor.SetBasePoint(basePoint)

        return Track(p1, v1, v2, p2)


    def CreateSwitch(self):
        # TODO: implement this
        pass
        



class AbstractTransform:
    """
    A transform does something with the geometry of track.
    """
    
    def __init__(self):
        pass


    def Transform(self, points, vectors):
        pass




class RightTrackTransform(AbstractTransform):

    def __init__(self, length, radius):
        AbstractTransform.__init__(self)
        self.radius = radius
        self.angle = length / radius


    def Transform(self, points, vectors):
        half = self.angle / 2
        cos_a = cos(half)
        sin_a = sin(half)

        matrix = [ \
            [cos_a, sin_a, 0.0], \
            [-sin_a, cos_a, 0.0], \
            [0.0, 0.0, 1.0]]

        for p in points:
            transformVec3(matrix, p)
            p.x = p.x + decimal.Decimal(str(self.radius))
        for v in vectors:
            transformVec3(matrix, v)

        self.Swap(points[0], points[1])
        self.Swap(vectors[0], vectors[1])


    def Swap(self, t1, t2):
        x, y, z = t1.x, t1.y, t1.z
        t1.x, t1.y, t1.z = t2.x, t2.y, t2.z
        t2.x, t2.y, t2.z = x, y, z




class LeftTrackTransform(AbstractTransform):

    def __init__(self, length, radius):
        AbstractTransform.__init__(self)
        self.radius = radius
        self.angle = length / radius


    def Transform(self, points, vectors):
        half = 0.5*self.angle
        cos_a = cos(-pi + half)
        sin_a = sin(-pi + half)

        matrix = [ \
            [cos_a, -sin_a, 0.0], \
            [sin_a, cos_a, 0.0], \
            [0.0, 0.0, 1.0]]

        for p in points:
            transformVec3(matrix, p)
            p.x = p.x + decimal.Decimal(str(-self.radius))
        for v in vectors:
            transformVec3(matrix, v)




class BasePointTransform(AbstractTransform):
    """
    Moves and rotates the geometry of track according base point.
    """

    def __init__(self, basePoint):
        AbstractTransform.__init__(self)
        self.point = basePoint.point
        self.alpha = -radians(basePoint.alpha)
        self.beta = atan(basePoint.gradient / 1000.0)


    def Transform(self, points, vectors):
        sin_a = sin(self.alpha)
        cos_a = cos(self.alpha)
        sin_b = sin(self.beta)
        cos_b = cos(self.beta)

        # Matrices for 3D transformations 
        matrix = [ \
            [cos_a, -sin_a, 0.0], \
            [cos_b*sin_a, cos_a*cos_b, -sin_b], \
            [sin_a*sin_b, sin_b*cos_a, cos_b]]

        for p in points:
            transformVec3(matrix, p)
            p.x = p.x + self.point.x
            p.y = p.y + self.point.y
            p.z = p.z + self.point.z
        for v in vectors:
            transformVec3(matrix, v)




def transformVec3(m, vec3):
    """
    Transforms Vec3 using matrix 4x4
    """
    x, y, z = float(vec3.x), float(vec3.y), float(vec3.z)

    vec3.x = decimal.Decimal(str(m[0][0] * x + m[0][1] * y + m[0][2] * z))
    vec3.y = decimal.Decimal(str(m[1][0] * x + m[1][1] * y + m[1][2] * z))
    vec3.z = decimal.Decimal(str(m[2][0] * x + m[2][1] * y + m[2][2] * z))

