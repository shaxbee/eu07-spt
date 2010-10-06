
from model.tracks import *
from model.scenery import *
from decimal import Decimal
from sptmath import Vec3
import math
import ui.trackfc
from ui.editor import BasePoint
import sptyaml
import yaml
import random
import datetime



class EditorMock:

    def __init__(self, p = Vec3('-50000.0', '50000.0', '0'), \
                 a = -math.pi/4):
        self.basePoint = BasePoint(p)

    def SetBasePoint(self, p, refresh = False):
        self.basePoint = p


def generateLargeScenery():
    """
    Generates large scenery.
    """
    scenery = Scenery()
    trackfc = ui.trackfc.TrackFactory(EditorMock())

    timeSum = datetime.timedelta 
    prefabsmap = yaml.load(file("prefabric.yaml", "r"), sptyaml.SptLoader)
    prefabs = []
    for l in prefabsmap.values():
        prefabs += l

    timeSum = datetime.timedelta()
    for n in range(1, 2000):
        e = random.choice(prefabs)
        handle = random.choice(e.handles)
        timeStart = datetime.datetime.now()

        t = trackfc.CopyRailTracking(e.railTracking, handle[0])
        scenery.AddRailTracking(t)

        timeEnd = datetime.datetime.now()
        delta = timeEnd - timeStart
        print "%d %.3f" % (n, float(delta.seconds + delta.microseconds / 1000000.0))
        timeSum += delta
                
    idelta = timeSum.days * 86400 + timeSum.seconds
    print "Insertations lasted %d sec" % idelta

    scenery_file = open("large.yaml", "w")
    scenery_file.write( yaml.dump(scenery) )
    scenery_file.close()




def generateSimpleScenery():
    scenery = Scenery()
    
    t1 = Track(p1 = Vec3(Decimal("1.164"), Decimal("21.003"), Decimal("0.0")), \
               p2 = Vec3(Decimal("1.825"), Decimal("26.966"), Decimal("0.0")))
    t2 = Track(Vec3(Decimal("0.0"), Decimal("0.0"), Decimal("0.0")), \
               Vec3(Decimal("0.0"), Decimal("-7.018"), Decimal("0.0")), \
               Vec3(Decimal("-0.776"), Decimal("6.974"), Decimal("0.0")), \
               Vec3(Decimal("1.164"), Decimal("-21.004"), Decimal("0.0")))
    t3 = Track(p1 = Vec3(Decimal("0.0"), Decimal("27.138"), Decimal("0.0")), \
               p2 = Vec3(Decimal("0.0"), Decimal("77.138"), Decimal("0.0")))
    t4 = Track(p1 = Vec3(Decimal("1.825"), Decimal("26.966"), Decimal("0.0")), \
               p2 = Vec3(Decimal("7.333"), Decimal("76.661"), Decimal("0.0")))
    
    r1 = Switch(pc = Vec3(Decimal("0.0"), Decimal("0.0"), Decimal("0.0")), \
                p1 = Vec3(Decimal("0.0"), Decimal("27.138"), Decimal("0.0")), \
                p2 = Vec3(Decimal("1.164"), Decimal("21.003"), Decimal("0.0")), \
                vc2 = Vec3(Decimal("0.0"), Decimal("7.017"), Decimal("0.0")), \
                v2 = Vec3(Decimal("-0.776"), Decimal("-6.974"), Decimal("0.0")))
    
    scenery.AddRailTracking(t1)
    scenery.AddRailTracking(t2)
    scenery.AddRailTracking(t3)
    scenery.AddRailTracking(t4)
    scenery.AddRailTracking(r1)
    
    # Configure yaml
    sptyaml.configureYaml()

    print yaml.dump(scenery)

if __name__ == "__main__":
    generateLargeScenery()

