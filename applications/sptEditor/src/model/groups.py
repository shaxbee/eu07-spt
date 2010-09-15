"""
Module containing definition of rails tracking elements' group. 

@author adammo
"""

import logging

import tracks
import sptmath


class RailContainer:
    """
    This is a container for rail tracking elements.
    """
    
    def __init__(self, name = None):
        # Contains all children
        self.children = []
        # Outline trackings are at borders of this container and may attach
        # to some external trackings.
        self.outline_trackings = []
        # A map containing points and external trackings
        self.connections = dict()

        self.name = name


    def __repr__(self):
        return "RailContainer[" \
            + "name=" + str(self.name) \
            + ", children=" + str(self.children) \
            + ", outlinePoints=" + str(self.connections.keys()) \
            + "]";


    def __eq__(self, other):
        if self is other:
            return True
        if other == None:
            return False
        if not isinstance(other, RailContainer):
            return False
        for tracking in self.children:
            if tracking not in other.children:
                return False
        return self.size() == other.size()

    
    def size(self):
        """
        Returns a number of rail trackings in group.
        """
        return len(self.children)


    def contains(self, tracking):
        """
        Checks if a group contains given rail tracking
        """
        return tracking in self.children


    def containsPoint(self, point):
        """
        Checks if specified point belongs to outline points.
        """
        return point in self.connections


    def getNormalVector(self, point):
        """
        Returns the normal vector for given outline point.
        """
        if not self.containsPoint(point):
            raise ValueError, "This point is not outline point"
        # Get the tracking that has this outline point
        internalTracking = None
        for t in self.outline_trackings:
            if t.containsPoint(point):
                internalTracking = t
        # And now compute normal vector on this track
        return internalTracking.getNormalVector(point)


    def getEndPoints(self):
        return self.connections.keys()


    def getGeometry(self):
        """
        Get all geometry points for all children
        """
        geo = []
        for t in self.children:
            geo += t.getGeometry()
        return geo


    def point2tracking(self, point):
        return self.connections[point]


    def nextPoint(self, point):
        """
        Compute next point for this rail tracking.
        """
        if not self.containsPoint(point):
            raise ValueError, "This point is not outline point"

        nextPoint = None

        # Get the first child from this container
        currentTracking = None
        for t in self.outline_trackings:
            if t.containsPoint(point):
                currentTracking = t

        if currentTracking is None:
            raise ValueError, "Current tracking not found in container"
        nextPoint = currentTracking.nextPoint(point)

        # Iterate though children
        while currentTracking in self.children \
                and currentTracking.point2tracking(nextPoint) is not None:            
            currentTracking = currentTracking.point2tracking(nextPoint)
            nextPoint = currentTracking.nextPoint(nextPoint)

        return nextPoint
            
        
    def insert(self, tracking):
        """
        Inserts given rail tracking into group.
        """
        _logger = logging.getLogger("Group")
        _logger.debug("Trying to insert " + str(tracking))

        if self.contains(tracking):
            raise ValueError, "Rail tracking is already in group"

        if not tracks.isDisconnected(tracking):
            raise ValueError, "Connected rail tracking cannot " \
                + "be inserted into group"

        geometry = tracking.getEndPoints()

        i = 0
        founds = 0L
        for gpoint in geometry:
            _logger.debug(("Processing %d geometry point " \
                + tracks.coord2str(gpoint)) % i)

            for child in self.children:
                if child.containsPoint(gpoint):
                    _logger.debug("Found following rail tracking that has " \
                        + "geometry point " + str(child))

                    v_tracking_normal = tracking.getNormalVector(gpoint)
                    v_child_normal = child.getNormalVector(gpoint)
                    
                    # Check if normal vectors may plug together
                    if sptmath.isNegativeVector(v_tracking_normal, v_child_normal):

                        # Check if connection to next rail tracking is empty
                        connInside = child.point2tracking(gpoint)
                        connOutside = self.connections[gpoint]

                        if connInside != None or connOutside != None:
                            # Connection in use, an error
                            raise Exception, "Inconsistent state"

                        _logger.debug("Setting connections for both " \
                            + "trackings")

                        founds |= (1 << i)

                        # Setup connections
                        child.setTracking(gpoint, tracking)
                        tracking.setTracking(gpoint, child)

                        # Remove rail tracking from outline if necessary
                        if child in self.outline_trackings \
                            and not self.isOutlineNow(child):
                            _logger.debug("Child found in outline " \
                                + "collections however it is inline now so " \
                                + "removing it form outlines")
                            self.outline_trackings.remove(child)

                        # Check geometry and remove outline point
                        if gpoint in self.connections:
                            _logger.debug("Removing geometry point from " \
                                + "outline points " \
                                + tracks.coord2str(gpoint))
                            del self.connections[gpoint]
                            break # Exit from for loop
                    else:
                        _logger.debug("At specified point " \
                            + tracks.coord2str(gpoint) + " vectors aren't " \
                            + "negative " \
                            + tracks.coord2str(v_tracking_normal) \
                            + ", " + tracks.coord2str(v_child_normal))

            if founds & (1 << i) == 0:
                _logger.debug("Adding specified point " \
                     + tracks.coord2str(gpoint) + " to outline points")
                self.connections[gpoint] = None

            i = i+1

        # Add whole rail tracking to outline trackings
        if sptmath.cardinality(founds, i) < len(geometry):
            _logger.debug(("Not all geometry points where bound " \
                + "to existing trackings. Found status %x. " \
                + "Adding tracking to outlines") % founds)
            self.outline_trackings.append(tracking)

        # Add to children
        self.children.append(tracking)

        _logger.debug("Rail tracking " + str(tracking) + " has successfully " \
            + "inserted into group")

        _logger.debug(self)


    def remove(self, tracking):
        """
        Removes rail tracking from group.
        """
        _logger = logging.getLogger("Group")
        _logger.debug("About to remove rail tracking " + str(tracking))

        if not self.contains(tracking):
            raise ValueError, "Rail tracking is not in this group"

        geometry = tracking.getEndPoints()

        # Check if the points don't make existing group connections
        for gpoint in geometry:
            if gpoint in self.connections and self.connections[gpoint] != None:
                raise ValueError, "Rail tracking is connected with another " \
                    " tracking on group level"

        i = 0
        for gpoint in geometry:
            _logger.debug(("Processing %d geometry point " \
                + tracks.coord2str(gpoint)) % i)

            previous = tracking.point2tracking(gpoint)

            if previous != None:
                _logger.debug("Unbinding previous tracking " + str(previous) \
                    + " found at point " + tracks.coord2str(gpoint))

                previous.setTracking(gpoint, None)
                tracking.setTracking(gpoint, None)

                # Add previous tracking to outline if it becomes outline now
                if previous not in self.outline_trackings:
                    _logger.debug("Adding previous tracking " + str(previous) \
                        + " to outlines")

                    self.outline_trackings.append(previous)

                _logger.debug("Adding point " + tracks.coord2str(gpoint) \
                    + " to outline points now")

                self.connections[gpoint] = None
            else:
                _logger.debug("Removing point " + tracks.coord2str(gpoint) \
                    + " from outline points, as there is no connected tracking")

                del self.connections[gpoint]

            i = i+1

        if tracking in self.outline_trackings:
            _logger.debug("Removing tracking " + str(tracking) \
                + " from outlines")

            self.outline_trackings.remove(tracking)

        self.children.remove(tracking)

        _logger.debug("Tracking " + str(tracking) + " was removed from group")

        _logger.debug(self)


    def isOutlineNow(self, tracking):
        geometry = tracking.getEndPoints()
        for p in geometry:
            if tracking.point2tracking(p) == None:
                return True
        return False


    def tracks(self):
        """
        Iterates over tracks in this rail container.
        """
        for c in self.children:
            if type(c) is tracks.Track:
                yield c
            elif type(c) is RailContainer:
                for c in c.tracks():
                    yield c


    def switches(self):
        """
        Iterates over switches in this rail container.
        """
        for c in self.children:
            if type(c) is tracks.Switch:
                yield c
            elif type(c) is RailContainer:
                for c in c.switches():
                    yield c
          

  

class RailGroup(RailContainer):
    """
    Rail tracking group.

    It is like a container of other rail trackings elements such tracks or
    rail switches and some other groups. Rail tracking group is also a
    rail tracking so it can be connected with another tracking elements.
    However rail tracking connections between the rail tracking outside
    group aren't propagated to the outline trackings inside group. So, for
    example, if the caller invoke {@link #toTracking(Point3d)} method on
    some outline tracking, he won't get the same result as in calling
    {@link #toTracking(Point3d)} method on group level.

    Beware that in in group there is an <em>outline tracking</em> concept
    which stays for the child tracking that has at least one unbound
    connection to next rail tracking. The <em>outline point</em> is a such
    geometry point of an outline tracking that has no connection bound. 
         
    Be also aware that changing geometry by not invoking methods
    {@link #mesh()} nor {@link #transform(Matrix4d)} may lead to some
    inconsistences and unpredictable results in some methods of this class.
    This is because geometry points are keys in connection mappings in group
    class. The are mutable, so they break {@link java.util.Map} assumptions.

    <h4>Logging</h4>
         
    Class support logging. If you want to see what happened while building
    this group, you may enable or create following logger (Apache commons
    logging):

    <p><code>
    pl.org.jet.track.RailTrackingGroup
    </code></p>
    """

    def __init__(self, name = None):
        RailContainer.__init__(self, name)


    def __repr__(self):
        return "RailGroup[" \
            + "name=" + str(self.name) \
            + ", children=" + str(self.children) \
            + ", outlinePoints=" + str(self.connections.keys()) \
            + "]";



