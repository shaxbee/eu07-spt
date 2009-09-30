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
        
        self.name = name
        
    def __repr__(self):
        return 'Group(name="%s", children=%s, outlinePoints=%s)' %(
            self.name,
            repr(self.__axleCounters),
            repr(self.__connections.keys())
            )
    
    def size(self):
        '''
        Returns number of axle counters containing in group
        '''
        return len(self.__axleCounters)
    
    def contains(self, axleCounter):
        '''
        Returns if axle counter is in list
        '''
        return axleCounter in self.__axleCounters
    
    def append(self, axleCounter):
        '''
        Insert new axle counter in list
        '''
        self.__axleCounters.append(axleCounter)

    def remove(self, axleCounter):
        '''
        Remove axle counter from list
        '''
        if not self.contains(axleCounter):
            raise ValueError("Group doesn't contain element %s" % str(axleCounter))

        self.__axleCounters.remove(axleCounter)
