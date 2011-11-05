'''
Module containing configuration elements of YAML processing engine.
It maps tags of YAML documents to Python classes

@author adammo
'''

import yaml

import model.tracks
import model.groups
import model.scenery
import sptmath
import model.vd.axleCounter

def __represent(dumper, data, name, attrs):
    return dumper.represent_mapping(
        name,
        dict((attr, getattr(data, attr)) for attr in attrs))
            
Track_attrs = ["p1", "v1", "v2", "p2"]
Switch_attrs = ["pc", "p1", "p2", "vc1", "vc2", "v1", "v2"]

Track_r_attrs = Track_attrs + ["name"]
Switch_r_attrs = Switch_attrs + ["name"]

def represent_Track(dumper, data):
    return __represent(dumper, data, "Track", Track_r_attrs)

def represent_Switch(dumper, data):
    return __represent(dumper, data, "Switch", Switch_r_attrs)

def represent_RailContainer(dumper, data):    
    return dumper.represent_mapping("RailContainer", \
        {"name": data.name,
         "children": list(data.children)})


def represent_Scenery(dumper, data):
    return __represent(dumper, data, "Scenery", ["tracks"])

def represent_Vec3(dumper, data):
    return dumper.represent_sequence("Vec3", (str(data.x), str(data.y), str(data.z)))

def represent_AxleCounter(dumper, data):
    return dumper.represent_mapping("AxleCounter", \
        {"id": data.getAxleCounterId(), \
         "railtracking": data.getRailTracking(), \
         "3dpoint": data.getGeometryPoint()})

class SptLoader(yaml.Loader):
    """
    Base YAML loader for SPT model classes.
    """

    def __init__(self, stream):
        yaml.Loader.__init__(self, stream)

        # This is a stack for parent rail containers if any
        self.__stack = []
        
        classes = ["Vec3", "Track", "Switch", "RailContainer", "AxleCounter", "Scenery"]

        for name in classes:
            self.add_constructor(name, getattr(self, "construct_" + name))
        
    def construct_Vec3(self, loader, node):
        (x, y, z) = loader.construct_sequence(node)
        return sptmath.Vec3(str(x), str(y), str(z))
        
    def __construct_RailTracking(self, loader, node, base_class, attrs):
        data = loader.construct_mapping(node, deep=False)
        result = base_class()
        
        for attr in attrs:
            setattr(result, attr, data[attr])
            
        if "name" in data:
            result.name = data["name"]
            
        if len(self.__stack) > 0:
            self.__stack[-1].insert(result)

        return result

    def construct_Track(self, loader, node):
        return self.__construct_RailTracking(loader, node, model.tracks.Track, Track_attrs)

    def construct_Switch(self, loader, node):
        return self.__construct_RailTracking(loader, node, model.tracks.Switch, Switch_attrs)

    def construct_RailContainer(self, loader, node):
        c = model.groups.RailContainer()
        self.__stack.append(c)

        map = loader.construct_mapping(node, deep=True)
        if "name" in map:
            c.name = map["name"]

        del self.__stack[-1]
        if len(self.__stack) > 0:
            self.__stack[-1].insert(c)
        return c

    def construct_Scenery(self, loader, node):
        s = model.scenery.Scenery()
        self.__stack = [s.tracks];
        map = loader.construct_mapping(node, deep=False)
        s.tracks = map["tracks"]
        return s

    def construct_AxleCounter(self, loader, node):
        map = loader.contruct_mapping(node, deep=False)
        a = model.vd.axleCounter.AxleCounter()
        a.__init__(map["id"])
        a.setGeometryPoint(map["3dpoint"])
        a.setRailTracking(map["railtracking"])
#        self.parent.insert(a)
        return a

# Dumper
yaml.add_representer(sptmath.Vec3, represent_Vec3)
yaml.add_representer(model.tracks.Track, represent_Track)
yaml.add_representer(model.tracks.Switch, represent_Switch)
yaml.add_representer(model.groups.RailContainer, represent_RailContainer)
yaml.add_representer(model.scenery.Scenery, represent_Scenery)
yaml.add_representer(model.vd.axleCounter.AxleCounter, represent_AxleCounter)
