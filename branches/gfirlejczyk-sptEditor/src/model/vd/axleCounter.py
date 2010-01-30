'''
Created on 2009-09-29

@author: gfirlejczyk
'''

class AxleCounter(object):
    '''
    Class handling axle counter like point that defines borders of VD Group
    '''


    def __init__(self, id = None):
        self.__id = id
        self.__geometryPoint = (0,0,0)
        self.__railTrackingID = 0
        
    def __repr__(self):
        return 'AxleCounter(id=%s, RailTrackingId=%s, GeometryPoint=%s)' %(
            self.__id,
            self.__geometryPoint,
            self.__railTrackingID)
    
    def setRailTracking(self,railTrackingId):
        '''Setting up railTrackingId which is connected to axle counter'''
        self.__railTrackingID = railTrackingId
    
    def getRailTracking(self):
        '''Returns RailTracking Id which is connected to axle counter'''
        return self.__railTrackingID

    def setGeometryPoint(self,geometryPoint):
        '''Set geometry point in 3d where axle counter is putting down'''
        self.__geometryPoint =  geometryPoint
    
    def getGeometryPoint(self):
        '''Get geometry point in 3d where axle counter is putting down'''
        return self.__geometryPoint
    
    def getAxleCounterId(self):
        '''Returns axle counter identification number'''
        return self.__id