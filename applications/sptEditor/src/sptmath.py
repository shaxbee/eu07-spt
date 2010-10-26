'''
Module containing dedicated math operations.

@author adammo
'''

import _sptmath

from wx import Point

Vec3 = _sptmath.FastVec3
Decimal = _sptmath.FastDec
dotProduct = _sptmath.dotProduct

if False:
    Vec3.__doc__ = \
        """
        A vector in 3D world.
        It uses fixed decimal point coordinates. It stores three decimal places.
        
        Setting x, y, z causes to quantize the value to one millimetre.

        Examples:
        >>> Vec3('0.001', '-0.001', '0.000')
        (0.001,-0.001,0.000)
        >>> a = Vec3('0.0001', '-0.0001', '0.000')
        >>> a
        (0.000,-0.000,0.000)
        >>> Vec3('0.999', '-0.999', '1.000')
        (0.999,-0.999,1.000)
        >>> b = Vec3('0.0005', '-0.0006', '-0.0004')
        >>> str(b.x)
        '0.001'
        >>> str(b.y)
        '-0.001'
        >>> str(b.z)
        '-0.000'
        >>> a + b
        (0.001,-0.001,0.000)
        >>> Vec3('0.9999', '-0.9999', '0.000')
        (1.000,-1.000,0.000)
        >>> Vec3('1.0001', '0.000', '-1.0001')
        (1.000,0.000,-1.000)
        >>> c = Vec3('0.0004', '-0.0004', '0.000')
        >>> c + c
        (0.000,-0.000,0.000)
        """

    Vec3.__eq__.__doc__ = \
        """
        Returns True if two Vec3 are equal.

        Note that Decimal -0.000 is equal with 0.000

        Examples:
        >>> Vec3("0.000", "-0.000", "0.000") == Vec3("-0.0", "0", "-0")
        True
        >>> Vec3("1.0", "-1.0", "0.001") == Vec3("1.000", "-1", "0.001")
        True
        >>> Vec3("2", "3", "-4.009") == Vec3("-2", "3.000", "-5")
        False
        """
            
    Vec3.moveBy.__doc__ = \
        """
        Moves this vector by given other v vector.

        Example:
        >>> a = Vec3('5.67', '34.43', '-898')
        >>> v = Vec3('-6', '34.44', '0.0004')
        >>> a.moveBy(-v)
        >>> a
        (11.670,-0.010,-898.000)
        >>> str(a.z)
        '-898.000'
        """
        
    Vec3.length.__doc__ = \
        """
        The length of the vector.
        """
        
    Vec3.dotProduct.__doc__ = \
        """
        Dot product of this vector and another.
        """

    Vec3.normalize.__doc__ = \
        """
        Normalizes the vector.

        Examples:
        >>> Vec3("1", "0", "0").normalize()
        (1.000,0.000,0.000)
        >>> Vec3("0", "-1", "0").normalize()
        (0.000,-1.000,0.000)
        >>> Vec3("-1", "-1", "0").normalize()
        (-0.707,-0.707,0.000)
        >>> Vec3("0.001", "0", "0").normalize()
        (1.000,0.000,0.000)
        >>> Vec3("-0.001", "-0.001", "0.001").normalize()
        (-0.577,-0.577,0.577)
        """

    Vec3.angleToJUnit.__doc__ = \
        """
        Returns the angle in radians to the unit vector J=(0, 1, 0).

        Examples:
        >>> str(Vec3("0", "1", "0").angleToJUnit())
        '0.0'
        >>> str(Vec3("1", "0", "0").angleToJUnit())
        '1.57079632679'
        >>> str(Vec3("-1", "0", "0").angleToJUnit())
        '4.71238898038'
        >>> str(Vec3("0", "-1", "0").angleToJUnit())
        '3.14159265359'
        >>> str(Vec3("1", "1", "0").angleToJUnit())
        '0.785398163397'
        >>> str(Vec3("-1", "1", "0").angleToJUnit())
        '5.49778714378'
        """        

    Vec3.scale.__doc__ = \
        """
        Scales the vector by scale s.

        Examples:
        >>> Vec3("1", "3", "0.5").scale(2)
        (2.000,6.000,1.000)
        >>> Vec3("-4", "0.001", "-0.999").scale(0.5)
        (-2.000,0.001,-0.500)
        >>> Vec3("0", "7", "-3").scale(-2)
        (-0.000,-14.000,6.000)
        >>> Vec3("5", "0.45", "-0.002").scale(0)
        (0.000,0.000,-0.000)
        """

    dotProduct.__doc__ = \
        """
        Dot product of two vectors.
        """

def isNegativeVector(a, b):
    """
    Checks if a spin of vector a is negative to spin of vector b.

    Examples:    
    >>> isNegativeVector(Vec3("1", "-1", "0"), Vec3("-1", "1", "0"))
    True
    >>> isNegativeVector(Vec3("-1", "-1", "0"), Vec3("2", "-2", "0"))
    False
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

    Examples:
    >>> cardinality(0x5cc5, 16)
    8
    >>> cardinality(0xf, 16)
    4
    >>> cardinality(0x0, 8)
    0
    >>> cardinality(0xf, 2)
    2
    """
    i = 0
    n = len-1
    while n >= 0:
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

    Example:    
    >>> sqDistanceTo([Point(3,3), Point(3,-3)], Point(0,-1))
    9.0
    >>> sqDistanceTo([Point(3,3), Point(3,-3)], Point(5,1))
    4.0
    >>> sqDistanceTo([Point(3,3), Point(3,-3)], Point(3,-5))
    4.0
    >>> sqDistanceTo([Point(3,3), Point(3,-3)], Point(3,0))
    0.0
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
            projLenSq = dotprod * dotprod / float(x2*x2 + y2*y2)
    lenSq = px*px + py*py - projLenSq
    if lenSq < 0.0:
        lenSq = 0.0
    return lenSq
    


