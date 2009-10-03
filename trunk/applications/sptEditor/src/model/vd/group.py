'''
Created on 2009-08-07

@author: gfirlejczyk
'''

class Group(object):
    '''
    Virtual Dispatcher Group for handling different types of SRK devices
    '''

    def __init__(self, name = None):
        self.__axleCounters = []
        self.__connections = dict()
        self.__srkDevices = dict()
        
        self.name = name
        
    def __repr__(self):
        return 'Group(name="%s", children=%s, outlinePoints=%s)' %(
            self.name,
            repr(self.__axleCounters),
            repr(self.__connections.keys())
            )
    
    def containsAxleCounter(self, axleCounter):
        '''
        Returns if axle counter is in list
        '''
        return axleCounter in self.__axleCounters
    
    def appendAxleCounter(self, axleCounter):
        '''
        Insert new axle counter in list
        '''
        self.__axleCounters.append(axleCounter)

    def removeAxleCounter(self, axleCounter):
        '''
        Remove axle counter from list
        '''
        if not self.contains(axleCounter):
            raise ValueError("Group doesn't contain element %s" % str(axleCounter))

        self.__axleCounters.remove(axleCounter)

    def containsSRKDevice(self, device):
        '''
        Check if given device is already connected to this group
        '''
        return device in self.__srkDevices
    
    def appendSRKDevice(self, device):
        '''
        Connect new device with the group
        '''
        self.__srkDevices[device.__id] = device
        
    def removeSRKDevice(self, device):
        '''
        Remove connection betwen group and srk device
        '''
        if not self.__srkDevices.__contains__(device.__id):
            raise ValueError("Group haven't connection to this device")
        
        del self.__srkDevices.device.__id
        