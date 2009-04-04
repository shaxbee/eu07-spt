'''
Module containing dedicated math operations.

@author adammo
'''

import math


def dotProduct(a, b):
    """
    Dot product of two vectors.
    """
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


def length(a):
    """
    The length of the vector.
    """
    return math.sqrt(a[0]**2 + a[1]**2 + a[2]**2)


def isNegativeVector(a, b):
    """
    Checks if a spin of vector a is negative to spin of vector b.
    """
    cosinus = dotProduct(a, b) / (length(a) * length(b))
    if cosinus < -1:
        cosinus = -1
    elif cosinus > 1:
        cosinus = 1
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

