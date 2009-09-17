'''
Created on 2009-08-07

@author: gfirlejczyk
'''
import model.tracks
import model.vd.element

class Group(object):
    '''
    Virtual Dispatcher Container for basic elements
    '''

    def __init__(selfparams, name = None):
        self.childrens = []
        self.connections = dict()
        
        self.name = name
        
    def __repr__(self):
        return 'Group(name="%s", children=%s, outlinePoints=%s)' %(
            self.name,
            repr(self.__children),
            repr(self.__connections.keys())
            )
    
    def size(self):
        """
        Returns number of elements containing in group
        """
        return len(self.__childrens)
    
    def contains(self, element):
        """
        Returns if vd_element is in children list
        """
        return element in self.__childrens
    
    def append(self, element):
        """
        Insert new VDElement in children list
        """
        self.__childrens.append(element)

    def remove(self, element):
        """
        Remove VDElement from this group
        """
        if not self.contains(element):
            raise ValueError("Group doesn't contain element %s" % str(element))

        self.__childrens.remove(element)
