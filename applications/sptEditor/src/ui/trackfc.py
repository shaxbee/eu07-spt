"""
Module containing various classes and functions that operates
on tracks within editor.

@author Adammo
"""

from math import sin, cos, tan, atan, radians, pi, degrees
import math
import copy

from sptmath import Vec3, Decimal
from model.tracks import Track
import model.groups
import ui.editor

class Vec3f:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

class TrackFactory:
    """
    Factory methods for tracks.
    """

    def __init__(self):
        #self.editor = editor
        self.basePoint = None
        pass
    
    def GetBasePoint(self):
        """
        Returning basePoint modified by Creating functions
        """
        return self.basePoint
    
    def CreateStraight(self, length, basePoint):
        
        p2 = Vec3f(0, length, length * basePoint.gradient / 1000.0)
        p1 = Vec3f()

        tr = BasePointTransform(basePoint)
        tr.RotateByAngleF([p1, p2], [])

        v1 = Vec3()
        v2 = Vec3()

        [p1, p2] = convertVec3ftoVec3([p1, p2])
        
        basePoint.point = p2

        # Refresh editor
        #self.editor.SetBasePoint(basePoint, True)
        self.basePoint = basePoint
        
        return Track(p1, v1, v2, p2)

    def CreateStraightOnStation(self, length, basePoint):
        
        p2 = Vec3f(0, length, 0)
        p1 = Vec3f()
        v1 = Vec3f()
        v2 = Vec3f()
        
        tr = BasePointTransform(basePoint)
        #tr.Transform([p1, p2], [v1, v2])
        tr.TransformF([p1, p2], [v1, v2])
        
        [p1, p2, v1, v2] = convertVec3ftoVec3([p1, p2, v1, v2])

        basePoint.point = p2

        # Refresh editor
        #self.editor.SetBasePoint(basePoint, True)
        self.basePoint = basePoint
        
        return Track(p1, v1, v2, p2)
    
    def CreateArc(self, angle, radius, isLeft, basePoint):
        """
        Creates curve track / helisa
        """
        length = radius * angle        
        bp = ui.editor.BasePoint(basePoint.point, basePoint.alpha, 0)

        track = self.CreateArcOnStation(angle, radius, isLeft, bp)

        track.p2.z = Decimal(length * basePoint.gradient / 1000.0)
        ctrl = 4.0 / 3.0 * radius * tan(angle * 0.25)
        track.v1.z = Decimal(ctrl * basePoint.gradient / 1000.0)
        track.v2.z = Decimal(ctrl * -basePoint.gradient / 1000.0)

        basePoint.SetAlpha(bp.alpha)
        basePoint.SetPosition(bp.point)

        return track

    def CreateArcOnStation(self, angle, radius, isLeft, basePoint):
        """
        Creates curve track
        """
        
        half = 0.5 * angle
        sin_a = sin(half)
        cos_a = cos(half)

        p1 = Vec3f(-radius * cos_a, radius * sin_a, 0)
        p2 = Vec3f(-radius * cos_a, -radius * sin_a, 0)

        ctrlX = (-radius * (4.0 - cos_a) / 3.0)
        ctrlY = (-radius * (1.0 - cos_a) * (cos_a - 3.0) / (3.0 * sin_a))

        v1 = Vec3f(ctrlX - p1.x, ctrlY - p1.y, (0))
        v2 = Vec3f(ctrlX - p2.x, -ctrlY - p2.y, (0))
        
        # Left or right
        tr = LeftTrackTransform(angle, radius) if isLeft \
            else RightTrackTransform(angle, radius)
        tr.TransformF([p1, p2], [v1, v2])

        #basePoint = self.editor.basePoint

        tr = BasePointTransform(basePoint)
        tr.TransformF([p1, p2], [v1, v2])
        
        [p1, p2, v1, v2] = convertVec3ftoVec3([p1, p2, v1, v2])
        
        basePoint.point = p2
        if isLeft:
            basePoint.alpha -= degrees(angle)
        else:
            basePoint.alpha += degrees(angle)

        # Refresh editor
        #self.editor.SetBasePoint(basePoint, True)
        self.basePoint = basePoint

        return Track(p1, v1, v2, p2)


    def CreateChangeOfGradient(self, target_gradient, radius, basePoint):
        """
        Create curve on change of gradient of line
        """
        alfa_home = math.atan2(basePoint.gradient,1000.0)
        alfa_target = math.atan2(target_gradient,1000.0)
        
        alfa = alfa_target - alfa_home

        T = math.fabs(radius * tan(alfa / 2))
        
        p1 = Vec3f()
        p2 = Vec3f()
        v1 = Vec3f()
        v2 = Vec3f()

        p2.y = (T + T*cos(alfa))
        p2.z = (T*sin(alfa))
        
        Lvec = 4.0/3.0*radius*tan(alfa/4.0)
        
        v1.x = p1.x
        v1.y = p1.y + (Lvec)
        v1.z = p1.z
        
        v2.x = p2.x
        v2.y = -(Lvec*cos(alfa))
        v2.z = -(Lvec*sin(alfa))
         
        tr = BasePointTransform(basePoint)
        tr.TransformF([p1, p2], [v1, v2])
        
        [p1, p2, v1, v2] = convertVec3ftoVec3([p1, p2, v1, v2])
        
        basePoint.point = p2
        basePoint.gradient = target_gradient
        self.basePoint = basePoint
        
        return Track(p1, v1, v2, p2)
    
    def CopyRailTracking(self, template, startPoint, basePoint):
        """
        Copies template rail tracking (single one or a group)
        into scenery.

        template = rail tracking to copy
        startPoint = Vec3 point within that template which is the insertation point.
        """

        #basePoint = self.editor.basePoint
        
        # 1. Make a copy of template
        tCopy = copy.deepcopy(template)

        # 2. Find the startPoint within copy
        if not tCopy.containsPoint(startPoint):
            raise ValueError, "Cannot find startPoint"

        # 3. Move to specified startPoint
        nVector = tCopy.getNormalVector(startPoint)

        nextPoint = tCopy.nextPoint(startPoint)

        tPoints = tCopy.getEndPoints()
        tGeo = tCopy.getGeometry()
        tVecs = [e for e in tGeo if e not in tPoints]

        for p in tPoints:
            p.moveBy(-startPoint)

        # 4. Rotate to specified startPoint
        angle = nVector.angleToJUnit()

        cos_a = cos(-angle - pi)
        sin_a = sin(-angle - pi)

        rMatrix = [ \
             [cos_a, sin_a, 0.0],
             [-sin_a, cos_a, 0.0],
             [0.0, 0.0, 1.0]]
        
        for g in tGeo:
            transformVec3(rMatrix, g)

        # 5-6. Rotate then to base point vector
        bpt = BasePointTransform(basePoint)
        bpt.Transform(tPoints, tVecs)

        # 7. Set the new position and vector of base point
        basePoint.point = Vec3(nextPoint.x, nextPoint.y, nextPoint.z)

        # Rail container, if yes rebuild
        if isinstance(tCopy, model.groups.RailContainer):
            tCopy.rebuild()

        nVector = tCopy.getNormalVector(nextPoint)
        angle = nVector.angleToJUnit()

        basePoint.alpha = degrees(angle)

        #self.editor.SetBasePoint(basePoint, True)
        self.basePoint = basePoint


        # Return copy
        return tCopy


    def CreateClosureTrack(self, startTrack, startPoint, endTrack, endPoint):
        """
        Creates closure tracks between two others.

        startTrack points to first track to connect and startPoint selects its geometry
        point.
        endTrack points to the second track to connect and its endPoint.
        """
        if not startTrack.containsPoint(startPoint):
            raise ValueError, "Start point is not defined in startTrack"
        if not endTrack.containsPoint(endPoint):
            raise ValueError, "End point is not defined in endTrack"

        # Get normal vectors
        startVec = startTrack.getNormalVector(startPoint)
        endVec = endTrack.getNormalVector(endPoint)

        length = (startPoint - endPoint).length()

        startVec = startVec.normalized()
        startVec = startVec.scaled(length * 0.333)
        endVec = endVec.normalized()
        endVec = endVec.scaled(length * 0.333)
        t = Track(p1 = startPoint, v1 = startVec, v2 = endVec, p2 = endPoint)
        return t



        
class AbstractTransform:
    """
    A transform does something with the geometry of track.
    """
    
    def __init__(self):
        pass


    def Transform(self, points, vectors):
        pass




class RightTrackTransform(AbstractTransform):

    def __init__(self, angle, radius):
        AbstractTransform.__init__(self)
        self.radius = radius
        self.angle = angle


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
            p.x = p.x + Decimal(self.radius)
        for v in vectors:
            transformVec3(matrix, v)

        self.Swap(points[0], points[1])
        self.Swap(vectors[0], vectors[1])

    def TransformF(self, points, vectors):
        half = self.angle / 2
        cos_a = cos(half)
        sin_a = sin(half)

        matrix = [ \
            [cos_a, sin_a, 0.0], \
            [-sin_a, cos_a, 0.0], \
            [0.0, 0.0, 1.0]]

        for p in points:
            transformVec3f(matrix, p)
            p.x = p.x + (self.radius)
        for v in vectors:
            transformVec3f(matrix, v)

        self.Swap(points[0], points[1])
        self.Swap(vectors[0], vectors[1])
        
    def Swap(self, t1, t2):
        x, y, z = t1.x, t1.y, t1.z
        t1.x, t1.y, t1.z = t2.x, t2.y, t2.z
        t2.x, t2.y, t2.z = x, y, z




class LeftTrackTransform(AbstractTransform):

    def __init__(self, angle, radius):
        AbstractTransform.__init__(self)
        self.radius = radius
        self.angle = angle


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
            p.x = p.x + Decimal(-self.radius)
        for v in vectors:
            transformVec3(matrix, v)

    def TransformF(self, points, vectors):
        half = 0.5*self.angle
        cos_a = cos(-pi + half)
        sin_a = sin(-pi + half)

        matrix = [ \
            [cos_a, -sin_a, 0.0], \
            [sin_a, cos_a, 0.0], \
            [0.0, 0.0, 1.0]]

        for p in points:
            transformVec3f(matrix, p)
            p.x = p.x + (-self.radius)
        for v in vectors:
            transformVec3f(matrix, v)


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
        matrix_gradient =[\
            [Decimal(1),Decimal(0),Decimal(0)], \
            [Decimal(0), Decimal(cos_b), Decimal(-sin_b)], \
            [Decimal(0), Decimal(sin_b), Decimal(cos_b)]]

        matrix_angle =[\
            [Decimal(cos_a), Decimal(-sin_a), Decimal(0)], \
            [Decimal(sin_a), Decimal(cos_a), Decimal(0)], \
            [Decimal(0), Decimal(0), Decimal(1)]]

        for p in points:
            transformVec3by2matrices(matrix_gradient,matrix_angle,p)
            #transformVec3(matrix_gradient, p)
            #transformVec3(matrix_angle, p)
            p+=self.point
            #p.x = p.x + self.point.x
            #p.y = p.y + self.point.y
            #p.z = p.z + self.point.z
            
        for v in vectors:
            transformVec3by2matrices(matrix_gradient,matrix_angle,v)
            #transformVec3(matrix_gradient, v)
            #transformVec3(matrix_angle, v)

    def TransformF(self, points, vectors):
        sin_a = sin(self.alpha)
        cos_a = cos(self.alpha)
        sin_b = sin(self.beta)
        cos_b = cos(self.beta)

        # Matrices for 3D transformations 

        matrix_gradient =[\
            [1,0,0], \
            [0, cos_b, -sin_b], \
            [0, sin_b, cos_b]]

        matrix_angle =[\
            [cos_a,-sin_a,0], \
            [sin_a, cos_a, 0], \
            [0, 0, 1]]
        
        for p in points:
            transformVec3fby2matrices(matrix_gradient,matrix_angle,p)
            #transformVec3f(matrix_all, p)
            p.x = p.x + float(self.point.x)
            p.y = p.y + float(self.point.y)
            p.z = p.z + float(self.point.z)
        
        for v in vectors:
            transformVec3fby2matrices(matrix_gradient,matrix_angle,v)
            #transformVec3f(matrix_gradient, v)
            #transformVec3(matrix_angle, v)
    
    
    def RotateByAngleF(self, points, vectors):
        """
        Rotate give'd points and vectors by angle of basepoint.
        Move give'd points to point of basepoint.
        """
        
        sin_a = sin(self.alpha)
        cos_a = cos(self.alpha)

        # Matrices for 3D transformations 

        matrix_angle =[\
            [cos_a,-sin_a,0], \
            [sin_a, cos_a, 0], \
            [0, 0, 1]]
        
        for p in points:
            transformVec3f(matrix_angle,p)
            p.x = p.x + float(self.point.x)
            p.y = p.y + float(self.point.y)
            p.z = p.z + float(self.point.z)
        
        for v in vectors:
            transformVec3f(matrix_angle,v)

    def RotateByAngle(self, points, vectors):
        """
        Rotate give'd points and vectors by angle of basepoint.
        Move give'd points to point of basepoint.
        """
        
        sin_a = sin(self.alpha)
        cos_a = cos(self.alpha)

        # Matrices for 3D transformations 

        matrix_angle =[\
            [Decimal(cos_a), Decimal(-sin_a), Decimal(0)], \
            [Decimal(sin_a), Decimal(cos_a), Decimal(0)], \
            [Decimal(0), Decimal(0), Decimal(1)]]
        
        for p in points:
            transformVec3(matrix_angle,p)
            p.x = p.x + (self.point.x)
            p.y = p.y + (self.point.y)
            p.z = p.z + (self.point.z)
        
        for v in vectors:
            transformVec3(matrix_angle,v)


def convertVec3ftoVec3(listVec3f):
    
    listVec3 = []
    
    for v in listVec3f:
        listVec3.append(Vec3(v.x, v.y, v.z))
        
    return listVec3

def transformVec3fby2matrices(m1, m2, vec):
    """
    Transform Vec3 by multiplaying by matrices m1 and next m2
    """
    
    #Convert vec3 to vec3f
    
    vec_f = Vec3f(vec.x.__float__(), vec.y.__float__(), vec.z.__float__())
    
    #rotating by matrix m1
    
    transformVec3f(m1, vec_f)
    
    #rotating by matrix m2
    
    transformVec3f(m2, vec_f)
    
    #Convert vec3f to vec3
    
    vec.x = (vec_f.x)
    vec.y = (vec_f.y)
    vec.z = (vec_f.z)
    
def transformVec3by2matrices(m1, m2, vec):
    """
    Transform Vec3 by multiplaying by matrices m1 and next m2
    """
    
    #Convert vec3 to vec3f
    
    #vec_f = Vec3f(vec.x.__float__(), vec.y.__float__(), vec.z.__float__())
    
    #rotating by matrix m1
    
    transformVec3(m1, vec)
    
    #rotating by matrix m2
    
    transformVec3(m2, vec)
    
    #Convert vec3f to vec3
    
    #vec.x = Decimal(vec_f.x)
    #vec.y = Decimal(vec_f.y)
    #vec.z = Decimal(vec_f.z) 
           
def transformVec3(m, vec3):
    """
    Transforms Vec3 using matrix 3x3
    """
    #x, y, z = float(vec3.x), float(vec3.y), float(vec3.z)
    x, y, z = (vec3.x), (vec3.y), (vec3.z)

    vec3.x = (m[0][0] * x + m[0][1] * y + m[0][2] * z)
    vec3.y = (m[1][0] * x + m[1][1] * y + m[1][2] * z)
    vec3.z = (m[2][0] * x + m[2][1] * y + m[2][2] * z)



def transformVec3f(m, vec):
    """
    Transforms Vec3 using matrix 3x3
    """
    x, y, z = float(vec.x), float(vec.y), float(vec.z)

    vec.x = m[0][0] * x + m[0][1] * y + m[0][2] * z
    vec.y = m[1][0] * x + m[1][1] * y + m[1][2] * z
    vec.z = m[2][0] * x + m[2][1] * y + m[2][2] * z

def transformVec3_4(m, vec3):
    """
    Transform Vec3 using 4x4 matrix.
    """
    x, y, z = float(vec3.x), float(vec3.y), float(vec3.z)

    vec3.x = Decimal(m[0][0] * x + m[0][1] * y + m[0][2] * z + m[0][3])
    vec3.y = Decimal(m[1][0] * x + m[1][1] * y + m[1][2] * z + m[1][3])
    vec3.z = Decimal(m[2][0] * x + m[2][1] * y + m[2][2] * z + m[2][3])
    
