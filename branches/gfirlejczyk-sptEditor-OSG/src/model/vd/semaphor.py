'''
Created on 2010-01-20

@author: gfirlejczyk
'''
import srkDevice

class semaphor(srkDevice.SRKDevice):
    '''
    Class contains semaphor device
    '''

    def __init__(self, id = None):
        '''
        Constructor
        '''
        self.__id = id
        
    def appendToGroup(self, vdGroupId = None):
        pass
    
    def removeFromGroup(self, vdGroupId = None):
        pass

    
    