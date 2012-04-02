Module containing dedicated math operations.
=============================================

First import necessary classes

    >>> from sptmath import Vec3, Decimal

Create Decimal:

    >>> Decimal('-4.434')
    Decimal('-4.434')
    >>> Vec3('3.343', '-4.434', '6.454')
    (3.343,-4.434,6.454)
    >>> Decimal('5')
    Decimal('5.000')
    >>> Decimal('-5')
    Decimal('-5.000')
    >>> Decimal('0')
    Decimal('0.000')
    >>> Decimal(0.5)
    Decimal('0.500')

Test Decimal operations:

    >>> Decimal(0.5) * 0.5
    Decimal('0.250')
    >>> Decimal(0.5) * -0.5
    Decimal('-0.250')
    >>> Decimal(2) * 1.25
    Decimal('2.500')

Copy Vec3:

    >>> import copy
    >>> vec = Vec3('1.0', '-1.0', '0.0')
    >>> vec == copy.deepcopy(vec)
    True

Test Vec3 core operations: 

    >>> Vec3('0.001', '-0.001', '0.000')
    (0.001,-0.001,0.000)
    >>> a = Vec3('0.0001', '-0.0001', '0.000')
    >>> a
    (0.000,0.000,0.000)
    >>> Vec3('0.999', '-0.999', '1.000')
    (0.999,-0.999,1.000)
    >>> b = Vec3('0.0005', '-0.0006', '-0.0004')
    >>> str(b.x)
    '0.001'
    >>> str(b.y)
    '-0.001'
    >>> str(b.z)
    '0.000'
    >>> a + b
    (0.001,-0.001,0.000)
    >>> Vec3('0.9999', '-0.9999', '0.000')
    (1.000,-1.000,0.000)
    >>> Vec3('1.0001', '0.000', '-1.0001')
    (1.000,0.000,-1.000)
    >>> c = Vec3('0.0004', '-0.0004', '0.000')
    >>> c + c
    (0.000,0.000,0.000)
    >>> d = Vec3('-3.673', '60.126', '0.000')
    >>> e = Vec3('-3.662', '32.989', '0.000')
    >>> d - e
    (-0.011,27.137,0.000)

Check Vec3 equality

    >>> Vec3("0.000", "-0.000", "0.000") == Vec3("-0.0", "0", "-0")
    True
    >>> Vec3("1.0", "-1.0", "0.001") == Vec3("1.000", "-1", "0.001")
    True
    >>> Vec3("2", "3", "-4.009") == Vec3("-2", "3.000", "-5")
    False

Moves this vector by given other v vector.

    >>> a = Vec3('5.67', '34.43', '-898')
    >>> v = Vec3('-6', '34.44', '0.0004')
    >>> a.moveBy(-v)
    >>> a
    (11.670,-0.010,-898.000)
    >>> str(a.z)
    '-898.000'

Normalizes the vector.

    >>> Vec3("1", "0", "0").normalized()
    (1.000,0.000,0.000)
    >>> Vec3("0", "-1", "0").normalized()
    (0.000,-1.000,0.000)
    >>> Vec3("-1", "-1", "0").normalized()
    (-0.707,-0.707,0.000)
    >>> Vec3("0.001", "0", "0").normalized()
    (1.000,0.000,0.000)
    >>> Vec3("-0.001", "-0.001", "0.001").normalized()
    (-0.577,-0.577,0.577)

Returns the angle in radians to the unit vector J=(0, 1, 0).

    >>> str(Vec3("0", "1", "0").angleToJUnit())
    '0.0'
    >>> str(round(Vec3("1", "0", "0").angleToJUnit(), 6))
    '1.570796'
    >>> str(round(Vec3("-1", "0", "0").angleToJUnit(), 6))
    '4.712389'
    >>> str(round(Vec3("0", "-1", "0").angleToJUnit(), 6))
    '3.141593'
    >>> str(round(Vec3("1", "1", "0").angleToJUnit(), 6))
    '0.785398'
    >>> str(round(Vec3("-1", "1", "0").angleToJUnit(), 6))
    '5.497787'

Scales the vector by scale s.

    >>> Vec3("1", "3", "0.5").scaled(2)
    (2.000,6.000,1.000)
    >>> Vec3("-4", "0.001", "-0.999").scaled(0.5)
    (-2.000,0.001,-0.500)
    >>> Vec3("0", "7", "-3").scaled(-2)
    (0.000,-14.000,6.000)
    >>> Vec3("5", "0.45", "-0.002").scaled(0)
    (0.000,0.000,0.000)

Internal representation of Decimal.

    >>> seq = [Decimal("-3"), Decimal("3"), Decimal("-3.000")]
    >>> [x.base() for x in seq]
    [1000, 1000, 1000]
    >>> [x.raw() for x in seq]
    [-3000L, 3000L, -3000L]

Test Decimal to_floor and to_ceiling.

    >>> seq = [Decimal("-1.001"), Decimal("-1"), Decimal("-0.999"),
    ...     Decimal("-0.001"), Decimal("0.000"), Decimal("0.001"),
    ...     Decimal("0.999"), Decimal("1.000"), Decimal("1.001")] 
    >>> [d.to_ceiling() for d in seq]
    [-1L, -1L, 0L, 0L, 0L, 1L, 1L, 1L, 2L]
    >>> [d.to_floor() for d in seq]
    [-2L, -1L, -1L, -1L, 0L, 0L, 0L, 1L, 1L]
