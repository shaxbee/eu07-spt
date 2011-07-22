'''
Module containing dedicated math operations.

@author adammo
'''

from wx import Point

try:
	from _sptmath import dotProduct, Vec3, Decimal
except ImportError:
	from _sptmathd import dotProduct, Vec3, Decimal
	
	
VEC3_ZERO = Vec3("0", "0", "0")


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
  
for sym in [Vec3, Decimal]:
    sym.__module__ = 'sptmath' 
    sym.__file__ = 'sptmath.cpp'

if __name__ == "__main__":
    import doctest
    doctest.testfile("sptmath.txt", optionflags=doctest.ELLIPSIS)
