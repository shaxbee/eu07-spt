'''
Module containing configuration elements of YAML processing engine.
It maps tags of YAML documents to Python classes

@author adammo
'''

import decimal
import yaml

import model.tracks
import model.groups
import model.scenery
import sptmath
import model.vd.axleCounter


def represent_Track(dumper, data):
    return dumper.represent_mapping("Track", \
        {"p1": data.p1, \
         "v1": data.v1, \
         "v2": data.v2, \
         "p2": data.p2, \
         "name": data.name, \
         })


def represent_Switch(dumper, data):
    return dumper.represent_mapping("Switch", \
        {"pc": data.pc,
         "p1": data.p1,
         "p2": data.p2,
         "v1": data.v1,
         "v2": data.v2,
         "vc1": data.vc1,
         "vc2": data.vc2,
         "name": data.name
	 })


def represent_RailContainer(dumper, data):
    return dumper.represent_mapping("RailContainer", \
        {"name": data.name,
         "children": data.children})


def represent_Scenery(dumper, data):
    return dumper.represent_mapping("Scenery", \
        {"tracks": data.tracks})


def represent_Vec3(dumper, data):
    return dumper.represent_sequence("Vec3", (str(data.x), str(data.y), str(data.z)))


def construct_Vec3(loader, node):
    (x, y, z) = loader.construct_sequence(node)
    return sptmath.Vec3(decimal.Decimal(x), decimal.Decimal(y), decimal.Decimal(z))

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
        
        self.add_constructor("Vec3", construct_Vec3)
        self.add_constructor("Track", self.construct_Track)
        self.add_constructor("Switch", self.construct_Switch)
        self.add_constructor("RailContainer", self.construct_RailContainer)
        self.add_constructor("AxleCounter", self.construct_AxleCounter)
        self.add_constructor("Scenery", self.construct_Scenery)


    def construct_Track(self, loader, node):
        map = loader.construct_mapping(node, deep=False)
        t = model.tracks.Track()
        t.p1 = map["p1"]
        t.v1 = map["v1"]
        t.v2 = map["v2"]
        t.p2 = map["p2"]
        if "name" in map:
            t.name = map["name"]
        if len(self.__stack) > 0:
            self.__stack[-1].insert(t)
        return t


    def construct_Switch(self, loader, node):
        map = loader.construct_mapping(node, deep=False)
        s = model.tracks.Switch()
        s.pc = map["pc"]
        s.p1 = map["p1"]
        s.p2 = map["p2"]
        s.vc1 = map["vc1"]
        s.vc2 = map["vc2"]
        s.v1 = map["v1"]
        s.v2 = map["v2"]
        if "name" in map:
            s.name = map["name"]
        if len(self.__stack) > 0:
            self.__stack[-1].insert(s)
        return s


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

