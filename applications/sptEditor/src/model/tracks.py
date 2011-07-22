"""
Created on 2009-03-04

@author: adammo
"""

from sptmath import Vec3, VEC3_ZERO

class RailTracking(object):
    """
    Abstract class for rail tracking.
    """

    def next(self, previous):
        """
        Returns next tracking element in scope of this tracking
        element for given previous tracking element.

        Implementators should throw special kind of runtime exception,
        UndeterminedTrackingException to indicate that this rail
        tracking element cannot determine next rail tracking element
        due to current connection state with other rail trackings.

        @param previous Previous tracking element.
        @type  previous RailTracking
        @return Next rail tracking or None.
        @rtype RailTracking
        """
        pass # Implement it in subclasses


    def nextPoint(self, point):
        """
        Returns next geometry point for this rail tracking element.
        """
        pass # Implement it in subclasses


    def point2tracking(self, point):
        """
        Gets the connected tracking element for given geometry point
        of this track element. If geometry point doesn't fit to this
        track geometry, method should throw ValueError.

        @param point A geometry point
        @return Corresponding connected tracking element or None if
          tracking element is not bound on this end to any tracking
          element.
        @rtype RailTracking
        """
        pass # Implement it in subclasses

    
    def tracking2point(self, tracking):
        """
        Sets at specified geoemtry point next rail tracking.
         
        Method may throw some {@link IllegalArgumentException} if for
        example point is null or rail tracking has already connected
        tracking at this point.
         
        Implementator classes shouldn't check if the next rail tracking
        is connected or not to some other rail trackings.

        @param p Geometry point to set up next rail tracking for this
          rail tracking. Point cannot be null and must be geometry point.
        @param next Next rail tracking to set up. It may be null to
          disconnect this rail tracking from the next one.
        """
        pass # Implement it in subclass


    def containsPoint(self, point):
        """
        Returns true if this rail tracking element has given geometry
        point.
        """
        pass # Implement it in subclasses


    def setTracking(self, point, next):
        """
        Sets at specified geoemtry point next rail tracking.
         
        Method may throw some ValueError if for
        example point is None or rail tracking has already connected
        tracking at this point.
         
        Implementator classes shouldn't check if the next rail tracking
        is connected or not to some other rail trackings.
         
        @param point Geometry point to set up next rail tracking for
          this rail tracking. Point cannot be null and must be geometry
          point.
        @param next Next rail tracking to set up. It may be null to
          disconnect this rail tracking from the next one.
        """
        pass # Implement it in subclasses


    def getGeometry(self):
        """
        Gets the 3d-geometry of the rail tracking.
        """
        pass # Implement it in subclasses


    def getEndPoints(self):
        """
        Get the 3d-geometry array of end points.
        """
        pass # Implement it in subclasses




class Track(RailTracking):
    """
    This is a track. Can be a straight track, an arc.
    """

    def __init__(self, p1=Vec3(), v1=Vec3(), v2=Vec3(), p2=Vec3()):
        """
        Constructor
        """
        self.p1 = p1
        self.v1 = v1
        self.v2 = v2
        self.p2 = p2
        
        self.n1 = None
        self.n2 = None

        self.name = None
        

    def __repr__(self):
        """
        Gives a detailed information about this object.
        """
        return "Track(name=%s, p1=%s, v1=%s, v2=%s, p2=%s)" % (
            str(self.name),
            repr(self.p1),
            repr(self.v1),
            repr(self.v2),
            repr(self.p2))
            
    def __eq__(self,other):
        """
        Compares this Track with another
        """
        if self is other:
            return True
        if not isinstance(other, Track):
            return False
        return self.p1 == other.p1 \
            and self.v1 == other.v1 \
            and self.v2 == other.v2 \
            and self.p2 == other.p2
            
        
    def next(self, previous):
        """
        Returns the next bound rail tracking.
        """
        if previous == None:
            if self.n1 != None and self.n2 != None:
                raise ValueError, "Previous RailTracking was null"
            elif self.n1 != None:
                return self.n1
            elif self.n2 != None:
                return self.n2
            else:
                raise UndeterminedTrackingException, "Undetermined RailTracking"
        
        if previous == self.n1:
            return self.n2
        elif previous == self.n2:
            return self.n1 

    
    def nextPoint(self, point):
        if self.p1 == point:
            return self.p2
        elif self.p2 == point:
            return self.p1

        raise ValueError, "Start point not found in geometry"


    def tracking2point(self, tracking):
        if tracking == None and self.n1 == None \
                and self.n2 == None:
            raise ValueError, "Cannot determine geometry point"
            
        if (tracking == None and self.n1 == None) \
                or (tracking != None and tracking == self.n1):
            return self.p1
        elif (tracking == None and self.n2 == None) \
                or (tracking != None and tracking == self.n2):
            return self.p2
        else:
            raise ValueError, "Tracking element is not bound"

    
    def point2tracking(self, point):
        if point == self.p1:
            return self.n1
        elif point == self.p2:
            return self.n2
        else:
            return None


    def containsPoint(self, point):
        return point == self.p1 or point == self.p2


    def setTracking(self, point, next):
        if point == None:
            raise ValueError, "Point is none"
        if not self.containsPoint(point):
            raise ValueError, "Point is not in geometry"

        if point == self.p1:
            self.n1 = next
        elif point == self.p2:
            self.n2 = next


    def getEndPoints(self):
        return [self.p1, self.p2]


    def getGeometry(self):
        return [self.p1, self.v1, self.v2, self.p2]


    def getNormalVector(self, point):
        """
        Gets a normal vector for given point
        """
        if point == self.p1:
            if not self.v1.x and not self.v1.y and not self.v1.z:
                return Vec3(self.p1.x - self.p2.x, \
                        self.p1.y - self.p2.y, \
                        self.p1.z - self.p2.z)
            else:
                return Vec3(-self.v1.x, -self.v1.y, -self.v1.z)
        elif point == self.p2:
            if not self.v2.x and not self.v2.y and not self.v2.z:
                return Vec3(self.p2.x - self.p1.x, \
                        self.p2.y - self.p1.y, \
                        self.p2.z - self.p1.z)
            else:
                return Vec3(-self.v2.x, -self.v2.y, -self.v2.z)
        else:
            return None




class Switch(RailTracking):
    """
    Rail switch class.
    """

    def __init__(self, pc=Vec3(), \
                       p1=Vec3(), \
                       p2=Vec3(), \
                       vc1=Vec3(), \
                       vc2=Vec3(), \
                       v1=Vec3(), \
                       v2=Vec3()):
        """
        Creates a switch.
        """

        self.pc = pc
        self.p1 = p1
        self.p2 = p2
        self.vc1 = vc1
        self.vc2 = vc2
        self.v1 = v1
        self.v2 = v2

        self.nc = None
        self.n1 = None
        self.n2 = None

        self.name = None


    def __repr__(self):
        """
        Gives a detailed information about this object.
        """
        return "Switch[" \
            + "name=" + str(self.name) \
            + ", pc=" + coord2str(self.pc) \
            + ", p1=" + coord2str(self.p1) \
            + ", p2=" + coord2str(self.p2) \
            + ", vc1=" + coord2str(self.vc1) \
            + ", v1=" + coord2str(self.v1) \
            + ", vc2=" + coord2str(self.vc2) \
            + ", v2=" + coord2str(self.v2) \
            + "]"


    def __eq__(self, other):
        """
        Compares this Switch with another
        """
        if self is other:
            return True
        if not isinstance(other, Switch):
            return False
        return self.pc == other.pc \
            and self.p1 == other.p1 \
            and self.p2 == other.p2 \
            and self.vc1 == other.vc1 \
            and self.v1 == other.v1 \
            and self.vc2 == other.vc2 \
            and self.v2 == other.v2


    def next(self, previous):
        if previous == None:
            if self.nc == None \
                    and self.n1 != None \
                    and self.n2 != None:
                return self.n1
            elif self.nc != None \
                    and ((self.n1 == None and self.n2 != None) \
                        or (self.n1 != None and self.n2 == None)):
                return self.nc
            else:
                raise UndeterminedTrackingException, "Previous rail tracking is null"

        if previous == self.nc:
            return self.n1
        elif previous == self.n1 or previous == self.n2:
            return self.nc

        raise ValueError, "Previous tracking not found"


    def nextPoint(self, start):
        if start == self.pc:
            return self.p1
        elif start == self.p1 or start == self.p2:
            return self.pc

        raise ValueError, "Start point not found in geometry"


    def tracking2point(self, tracking):
        bits = 0

        if tracking == self.nc \
            or (tracking != None and tracking == self.nc):
            bits |= 1
        if tracking == self.n1 \
            or (tracking != None and tracking == self.n1):
            bits |= 2
        if tracking == self.n2 \
            or (tracking != None and tracking == self.n2):
            bits |= 4

        if bits == 1:
            return self.pc
        elif bits == 2:
            return self.p1
        elif bits == 4:
            return self.p2
        else:
            raise ValueError, "Tracking element in not bound"


    def point2tracking(self, point):
        if point == self.pc:
            return self.nc
        elif point == self.p1:
            return self.n1
        elif point == self.p2:
            return self.n2
        else:
            return None


    def containsPoint(self, point):
        return point == self.pc or point == self.p1 or point == self.p2


    def setTracking(self, point, next):
        if point == None:
            raise ValueError, "Point is null"
        if not self.containsPoint(point):
            raise ValueError, "Point is not in geometry"

        if point == self.pc:
            self.nc = next
        elif point == self.p1:
            self.n1 = next
        elif point == self.p2:
            self.n2 = next


    def getEndPoints(self):
        return [self.pc, self.p1, self.p2]


    def getGeometry(self):
        return [self.pc, self.vc1, self.v1, self.p1, self.vc2, self.v2, self.p2]


    def getNormalVector(self, point):
        if point == self.pc:
            if self.vc1 == VEC3_ZERO:
                return Vec3(self.pc.x - self.p1.x, \
                        self.pc.y - self.p1.y, \
                        self.pc.z - self.p1.z)
            else:
                return Vec3(-self.vc1.x, -self.vc1.y, -self.vc1.z)
        elif point == self.p1:
            if self.v1 == VEC3_ZERO:
                return Vec3(self.p1.x - self.pc.x, \
                        self.p1.y - self.pc.y, \
                        self.p2.z - self.pc.z)
            else:
                return Vec3(-self.v1.x, -self.v1.y, -self.v1.z)
        elif point == self.p2:
            if self.v2 == VEC3_ZERO:
                return Vec3(self.p2.x - self.pc.x, \
                        self.p2.y - self.pc.y, \
                        self.p2.z - self.p2.z)
            else:
                return Vec3(-self.v2.x, -self.v2.y, -self.v2.z)
        else:
            return None




class UndeterminedTrackingException(Exception):
    """
    Exception indicating problem with determining next track.
    """

    def __init__(self, message = None):
        self.message = message

    
    def __str__(self):
        return repr(self.message)




def coord2str(coord):
    """
    Formats tuple (coordinate) into string.
    """
    return "(%(x).3f,%(y).3f,%(z).3f)" % \
        {'x': coord.x, 'y': coord.y, 'z': coord.z}


def isDisconnected(tracking):
    """
    Checks if given rail tracking element is disconnected.

    Disconnected track means such rail tracking element
    that isn't connected to any other rail trackings.
    """
    geometry = tracking.getEndPoints()
    for p in geometry:
        if tracking.point2tracking(p) != None:
            return False
    return True


