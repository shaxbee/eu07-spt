'''
Module containing dedicated math operations.

@author adammo
'''

import math
from decimal import Decimal

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
        _length = self.length()
        self.x = self.x / _length
        self.y = self.y / _length
        self.z = self.z / _length


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

