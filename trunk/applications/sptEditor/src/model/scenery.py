'''
Module containing the scenery.
Scenery contains all elements that build the railways world in
the simulator.

@author adammo
'''

import groups
import tracks

class Scenery:
    '''
    Scenery.
    '''

    def __init__(self):
        self.tracks = groups.Group()


    def AddRailTracking(self, tracking):
        self.tracks.insert(tracking)


    def RemoveRailTracking(self, tracking):
        if self.tracks.contains(tracking):
            return

        self.tracks.remove(tracking)


    def RailTrackingIterator(self):
        return self.tracks.children

