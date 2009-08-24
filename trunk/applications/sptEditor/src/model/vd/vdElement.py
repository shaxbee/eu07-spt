'''
Created on 2009-08-09

@author: gfirlejczyk
'''

class VDElement(object):
    """
    Virtual Dispatcher basic element
    """
    
    def __init__(selfparams, name = None):
        """
        Constructor
        """
        
    def __repr__(self):
       return "VDElement[" \
        + "name=" + str(self.name) \
        + ", Base class]"
        
    def size(self):
        """
        Returns number of RailTrackings contained in this class
        """
        return 0
    
    def insert(rail_tracking):
        '''
        Add new member of RailTracking object to VDElement
        '''
        pass
