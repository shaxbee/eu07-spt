'''
Created on 2009-08-07

@author: gfirlejczyk
'''
import tracks.py
import vdElement.py

class VDGroup(object):
    '''
    Virtual Dispatcher Container for basic elements
    
    
    '''

    def __init__(selfparams, name = None):
        '''
        Constructor
        '''
        self.children = []
        self.connections = dict()
        
        self.name = name
        
    def __repr__(self):
       return "VDGroup[" \
        + "name=" + str(self.name) \
        + ", children=" + str(self.children) \
        + ", outlinePoints=" + str(self.connections.keys()) \
        + "]";
    
    def size(self):
        """
        Returns number of elements containing in group
        """
        return len(self.children)
    
    def contains(self, vd_element):
        """
        Returns if vd_element is in children list
        """
        return vd_element in self.children
    
    def insert(self, vd_element):
        """
        Insert new VDElement in children list
        """
        self.children.append(vd_element)

    def remove(self, vd_element):
        """
        Remove VDElement from this group
        """
        if not self.contains(vd_element):
            raise ValueError, "Group doesn't contains this element"

        self.children.remove(vd_element)
