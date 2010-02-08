'''
Created on 2009-10-10

@author: gfirlejczyk
'''

class SRKDevice(object):
    '''
    Virtual class for all srk devices included to scenery
    '''


    def __init__(self, id = None):
        self.__id = id
        
    def __repr__(self):
        pass
    
    def appendToGroup(self, vdGroupId = None):
        pass
    
    def removeFromGroup(self, vdGroupId = None):
        pass
