'''
Module containing dedicated math operations

@author adammo
'''

def dotProduct(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def length(a):
    return sqrt(a[0]**2 + a[1]**2 + a[2]**2)

def isNegativeVector(a, b):
    cosinus = dotProduct(a, b) / (length(a) * length(b))
    if cosinus < -1:
        cosinus = -1
    elif consinus > 1:
        cosinus = 1
    return cosinus < -0.9997

def cardinality(value, len):
    i = 0
    n = len
    while n > 0:
        if (value & (1 << n)) > 0:
            i = i+1
        n = n-1
    return i

