'''
Module containing dedicated math operations.

@author adammo
'''

import math
from decimal import Decimal
from wx import Point

THREE_POINTS = Decimal('1.000')


class Vec3:
    """
    A vector in 3D world.
    It uses fixed decimal point coordinates. It stores three decimal places.
    """

    def __init__(self, x = Decimal(0), y = Decimal(0), z = Decimal(0)):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "(%.3f,%.3f,%.3f)" % (self.x, self.y, self.z)

    def __eq__(self, other):
        if other == None:
            return False
        if not isinstance(other, Vec3):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return 37 + hash(self.x)*7 + hash(self.y)*11 + hash(self.z)*3

    def __setattr__(self, name, arg):
        """
        Setting x,y,z causes to quantize the value
        """
        if arg is None:
           raise ValueError()
        if type(arg) == str:
           arg = Decimal(arg)
        self.__dict__[name] = arg.quantize(THREE_POINTS)

    def __add__(self, arg):
       x = self.x + arg.x
       y = self.y + arg.y
       z = self.z + arg.z
       return Vec3(x, y, z)

    def __sub__(self, arg):
       x = self.x - arg.x
       y = self.y - arg.y
       z = self.z - arg.z
       return Vec3(x, y, z)

    def __neg__(self):
       return Vec3(-self.x, -self.y, -self.z)

    def moveBy(self, v):
       self.x = self.x + v.x
       self.y = self.y + v.y
       self.z = self.z + v.z

    def length(self):
        """
        The length of the vector.
        """
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

    def dotProduct(self, other):
        """
        Dot product of this vector and another.
        """
        return float(self.x*other.x + self.y*other.y + self.z*other.z)

    def normalize(self):
        """
        Normalizes the vector
        """
        _length = length()
        self.x = self.x / _length
        self.y = self.y / _length
        self.z = self.z / _length

    def angleToJUnit(self):
        """
        Returns the angle in radians to the unit vector J=(0, 1, 0).
        """
        theta = math.acos(float(self.y) / self.length())
        if self.x <= -0.0:
            return theta
        else:
            return -theta




def dotProduct(a, b):
    """
    Dot product of two vectors.
    """
    return float(a.x*b.x + a.y*b.y + a.z*b.z)


def isNegativeVector(a, b):
    """
    Checks if a spin of vector a is negative to spin of vector b.
    """
    cosinus = dotProduct(a, b) / (a.length() * b.length())
    if cosinus < -1.0:
        cosinus = -1.0
    elif cosinus > 1.0:
        cosinus = 1.0
    return cosinus < -0.9997


def cardinality(value, len):
    """
    Number of bits set in integer value.
    """
    i = 0
    n = len
    while n > 0:
        if (value & (1 << n)) > 0:
            i = i+1
        n = n-1
    return i


def toLineSegments(bezier, level = 4):
    """
    Transforms cubic bezier curve (defined as 4-element array of Points)
    to line segments.
    It recursively divides bezier curve level times.

    Returns array of Points.
    """
    result = [bezier[0]]
    recursivelyToLineSegments(bezier, level, result)
    result += [bezier[3]]
    return result
    
   
BISECT_TOLERANCE = 5 
 
def recursivelyToLineSegments(bezier, level, result):
    if level == 0:
        return

    x12 = (bezier[0].x + bezier[1].x) / 2
    y12 = (bezier[0].y + bezier[1].y) / 2
    x23 = (bezier[1].x + bezier[2].x) / 2
    y23 = (bezier[1].y + bezier[2].y) / 2
    x34 = (bezier[2].x + bezier[3].x) / 2
    y34 = (bezier[2].y + bezier[3].y) / 2
    x123 = (x12 + x23) / 2
    y123 = (y12 + y23) / 2
    x234 = (x23 + x34) / 2
    y234 = (y23 + y34) / 2
    x1234 = (x123 + x234) / 2
    y1234 = (y123 + y234) / 2

    dx = bezier[3].x - bezier[0].x
    dy = bezier[3].y - bezier[0].y

    d2 = abs((bezier[1].x - bezier[3].x) * dy - (bezier[1].y - bezier[3].y) * dx)
    d3 = abs((bezier[2].x - bezier[3].x) * dy - (bezier[2].y - bezier[3].y) * dx)

    if (d2+d3)*(d2+d3) < BISECT_TOLERANCE*(dx*dx + dy*dy):
        result += [Point(x1234, y1234)]
    else:
        recursivelyToLineSegments([bezier[0], Point(x12, y12), Point(x123, y123), Point(x1234, y1234)], \
            level-1, result)
        recursivelyToLineSegments([Point(x1234, y1234), Point(x234, y234), Point(x34, y34), bezier[3]], \
            level-1, result)


def sqDistanceTo(line, point):
    """
    Returns squared distance of line and point (defined as wx.Points)

    Example
    >>> sqDistanceTo([wx.Point(3,3), wx.Point(3,-3)], wx.Point(0, -1))
    3.0
    """
    x1, y1 = line[0].x, line[0].y
    x2, y2 = line[1].x, line[1].y
    px, py = point.x, point.y
    x2 -= x1
    y2 -= y1
    px -= x1
    py -= y1
    dotprod = px*x2 + py*y2
    projLenSq = 0.0
    if dotprod <= 0.0:
        projLenSq = 0.0
    else:
        px = x2 - px
        py = y2 - py
        dotprod = px*x2 + py*y2
        if dotprod <= 0.0:
            projLenSq = 0.0
        else:
            projLenSq = dotprod * dotprod / (x2*x2 + y2*y2)
    lenSq = px*px + py*py - projLenSq
    if lenSq < 0.0:
        lenSq = 0.0
    return lenSq
    


