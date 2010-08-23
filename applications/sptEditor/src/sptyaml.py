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

def configureYaml():
    # Loader
    loader = SceneryLoader()
    yaml.add_constructor("Vec3", construct_Vec3)
    yaml.add_constructor("Track", loader.construct_Track)
    yaml.add_constructor("Switch", loader.construct_Switch)
    yaml.add_constructor("RailContainer", loader.construct_RailContainer)
    yaml.add_constructor("Scenery", loader.construct_Scenery)
    yaml.add_constructor("AxleCounter", loader.construct_AxleCounter)
    
    # Dumper
    yaml.add_representer(sptmath.Vec3, represent_Vec3)
    yaml.add_representer(model.tracks.Track, represent_Track)
    yaml.add_representer(model.tracks.Switch, represent_Switch)
    yaml.add_representer(model.groups.RailContainer, represent_RailContainer)
    yaml.add_representer(model.scenery.Scenery, represent_Scenery)
    yaml.add_representer(model.vd.axleCounter.AxleCounter, represent_AxleCounter)


def represent_Track(dumper, data):
    return dumper.represent_mapping("Track", \
        {"p1": data.p1, \
         "v1": data.v1, \
         "v2": data.v2, \
         "p2": data.p2, \
#         "n1": data.n1, \
#         "n2": data.n2})
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
#         "nc": data.nc,
#         "n1": data.n1,
#         "n2": data.n2})
         "name": data.name
	 })


def represent_RailContainer(dumper, data):
    return dumper.represent_mapping("RailContainer", \
        {"name": data.name,
         "children": data.children,
         "outline": data.outline_trackings,
         "connections": data.connections})


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


class SceneryLoader:

    def __init__(self):
        self.parent = None

    def construct_Track(self, loader, node):
        map = loader.construct_mapping(node, deep=False)
        t = model.tracks.Track()
        t.p1 = map["p1"]
        t.v1 = map["v1"]
        t.v2 = map["v2"]
        t.p2 = map["p2"]
        t.name = map["name"]
        if self.parent != None:
            self.parent.insert(t)
#        t.n1 = map["n1"]
#        t.n2 = map["n2"]
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
        s.name = map["name"]
        if self.parent != None:
            self.parent.insert(s)
#        s.nc = map["nc"]
#        s.n1 = map["n1"]
#        s.n2 = map["n2"]
        return s


    def construct_RailContainer(self, loader, node):
        map = loader.construct_mapping(node, deep=False)
        c = model.groups.RailContainer()
        c.name = map["name"]
        c.children = map["children"]
        c.outline_trackings = map["outline"]
        c.connections = map["connections"]
        if self.parent != None:
            self.parent.insert(c)
        self.parent = c
        return c


    def construct_Scenery(self, loader, node):
        map = loader.construct_mapping(node)
        s = model.scenery.Scenery()
        s.tracks = map["tracks"]
        self.parent = s.tracks
        return s
    
    
    def construct_AxleCounter(self, loader, node):
        map = loader.contruct_mapping(node, deep=False)
        a = model.vd.axleCounter.AxleCounter()
        a.__init__(map["id"])
        a.setGeometryPoint(map["3dpoint"])
        a.setRailTracking(map["railtracking"])
#        self.parent.insert(a)
        return a
        


