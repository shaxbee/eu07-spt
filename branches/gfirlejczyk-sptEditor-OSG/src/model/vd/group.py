'''
Created on 2009-08-07

@author: gfirlejczyk
'''

import axleCounter
import srkDevice

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
    
    def containsAxleCounter(self, axleCounter = axleCounter.AxleCounter()):
        '''
        Returns if axle counter is in list
        '''
        return axleCounter in self.__axleCounters
    
    def appendAxleCounter(self, axleCounter = axleCounter.AxleCounter()):
        '''
        Insert new axle counter in list
        '''
        self.__axleCounters.append(axleCounter)

    def removeAxleCounter(self, axleCounter = axleCounter.AxleCounter()):
        '''
        Remove axle counter from list
        '''
        if not self.contains(axleCounter):
            raise ValueError("Group doesn't contain element %s" % str(axleCounter))

        self.__axleCounters.remove(axleCounter)

    def containsSRKDevice(self, device = srkDevice.SRKDevice()):
        '''
        Check if given device is already connected to this group
        '''
        return device in self.__srkDevices
    
    def appendSRKDevice(self, device = srkDevice.SRKDevice()):
        '''
        Connect new device with the group
        '''
        self.__srkDevices[device.__id] = device
        
    def removeSRKDevice(self, device = srkDevice.SRKDevice()):
        '''
        Remove connection between group and srk device
        '''
        if not self.__srkDevices.__contains__(device.__id):
            raise ValueError("Group haven't connection to this device")
        
        del self.__srkDevices.device.__id
        