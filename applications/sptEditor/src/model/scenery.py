"""
Module containing the scenery.
Scenery contains all elements that build the railways world in
the simulator.

@author adammo
"""

import groups
import tracks

class Scenery:
    """ 
    Scenery defines world begin simulated.
    """
    
    def __init__(self):
        self.listeners = []
        self.tracks = groups.RailContainer()


    def AddRailTracking(self, tracking):
        self.tracks.insert(tracking)
        self.FireSceneryChange(SceneryEvent(self, CHANGE_ADD, tracking))


    def RemoveRailTracking(self, tracking):
        if self.tracks.contains(tracking):
            return

        self.tracks.remove(tracking)
        self.FireSceneryChange(SceneryEvent(self, CHANGE_REMOVE, tracking))


    def RailTrackingIterator(self):
        return self.tracks.children


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


    def FireSceneryChange(self, event):
        """
        Notifies registered listeners about the change.
        """
        for l in self.listeners:
            l.sceneryChanged(event)




class SceneryListener:
    """
    Listener interface for listening changes in scenery.
    """

    def __init__(self):
        pass


    def sceneryChanged(self, event):
        """
        Implementators should override this method.
        """
        pass




# The constants for scenery event
CHANGE_ADD = 1
CHANGE_REMOVE = 2

class SceneryEvent:
    """
    This object encapsulates single modification of scenery.

    Note that class contract may be extended for example to several
    changes at once.
    """

    def __init__(self, scenery, type, element):
        self.scenery = scenery
        self.type = type
        self.element = element


    def GetScenery(self):
        return self.scenery


    def GetType(self):
        return self.type


    def GetElement(self):
        return self.element

