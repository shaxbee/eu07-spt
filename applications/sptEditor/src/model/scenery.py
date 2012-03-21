"""
Module containing the scenery.
Scenery contains all elements that build the railways world in
the simulator.

@author adammo
"""

import groups
#import tracks
from sptmath import Vec3

class Scenery:
    """ 
    Scenery defines world being simulated.
    """
    
    def __init__(self):
        self.listeners = []
        self.tracks = groups.RailContainer()


    def AddRailTracking(self, tracking):
        """
        Adds a new rail tracking to the scenery.
        """
        self.tracks.insert(tracking)
        self.FireSceneryChange(SceneryListener.Add, tracking)


    def RemoveRailTracking(self, tracking):
        if not self.tracks.contains(tracking):
            return

        self.tracks.remove(tracking)
        self.FireSceneryChange(SceneryListener.Remove, tracking)


    def RailTrackingIterator(self):
        return self.tracks.children
    
    
    def GetMbc(self):
        return self.tracks.children.getMbc()
    
    
    def Query(self, vp):
        return self.tracks.children.queryView(vp)
    
    
    def QueryPoint(self, p):
        assert isinstance(p, Vec3)
        return self.tracks.children.queryPoint(p.x, p.y, p.z)


    def RegisterListener(self, listener):
        """
        Registers a listener in this scenery.
        """
        self.listeners.append(listener)


    def UnregisterListener(self, listener):
        """
        Unregisters previously registered listener.
        """
        self.listeners.remove(listener)


    def FireSceneryChange(self, event, element):
        """
        Notifies registered listeners about the change.
        """
        for l in self.listeners:
            event(l, self, element)

class SceneryListener:
    """
    Listener interface for listening changes in scenery.
    """

    def __init__(self):
        pass

    def Add(self, scenery, element):
        pass

    def Remove(self, scenery, element):
        pass

