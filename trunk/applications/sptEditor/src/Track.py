'''
Created on 2009-03-04

@author: adammo
'''

class Track(object):
    '''
    This is a track
    '''

    def __init__(self, p1=(0.0, 0.0, 0,0), v1=(0.0, 0.0, 0.0), v2=(0.0, 0.0, 0.0), p2=(0.0, 0.0, 0.0)):
        '''
        Constructor
        '''
        self.p1 = p1
        self.v1 = v1
        self.v2 = v2
        self.p2 = p2
        
        self.p1_tracking = None
        self.p2_tracking = None
        
        
    def coord2str(self, coord):
        '''
        Formats tuple (coordinate) into string.
        '''
        return "(%(x).3f,%(y).3f,%(z).3f)" % \
            {'x': coord[0], 'y': coord[1], 'z': coord[2]}
        

    def __repr__(self):
        '''
        Gives a detailed information about this object.
        '''
        return "Track[" \
            + "p1=" + self.coord2str(self.p1) \
            + ", v1=" + self.coord2str(self.v1) \
            + ", v2=" + self.coord2str(self.v2) \
            + ", p2=" + self.coord2str(self.p2)
            
    def __eq__(self,other):
        '''
        Compares this Track with another
        '''
        if self is other:
            return True
        if not isinstance(other, Track):
            return False
        return self.p1 == other.p1 \
            and self.v1 == other.v1 \
            and self.v2 == other.v2 \
            and self.p2 == other.p2
            
        
    def next(self, previous):
        '''
        Returns the next bound rail tracking.
        '''
        if previous == None:
            if self.p1_tracking != None and self.p2_tracking != None:
                raise ValueError, "Previous RailTracking was null"
            elif self.p1_tracking != None:
                return self.p1_tracking
            elif self.p2_tracking != None:
                return self.p2_tracking
            else:
                raise Exception, "Undetermined RailTracking"
        
        if previous == self.p1_tracking:
            return self.p2_tracking
        elif previous == self.p2_tracking:
            return self.p1_tracking 
        