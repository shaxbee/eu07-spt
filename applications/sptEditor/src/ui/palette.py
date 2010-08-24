"""
Module containing palettes
"""

import yaml
import wx
import sptyaml
from sptmath import Vec3
from model.tracks import Track, Switch


class TrackPalette(wx.Panel):
    """
    Track palette
    """


    def __init__(self, parent, id = wx.ID_ANY):
        wx.Panel.__init__(self, parent, id)


    def LoadPrefabs(self):
        pass


    def VerifyPrefabs(self):
        pass


class TrackingItem:
    """
    An item of track palette.
    """

    """
    Textual description - searchable
    """
    description = dict()
    """
    List of handles. Each element is a tuple of
    Vec3 and the icon description
    """
    handles = list()
    """
    Rail tracking to insert
    """
    railTracking = None

    def __init__(self):
        pass


    def __repr__(self):
        sb = u""
        for k, v in self.description.iteritems():
            sb = sb + unicode(k) + u" " + unicode(v) + u" "
        return sb


    def Verify(self):
        for p in map(lambda h: h[0] in self.handles):
            if not self.railTracking.containsPoint(p):
                return False
        return True

