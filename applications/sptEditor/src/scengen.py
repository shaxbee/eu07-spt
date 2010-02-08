
from model.tracks import *
from model.scenery import *
from decimal import Decimal
from sptmath import Vec3
import sptyaml
import yaml 


if __name__ == '__main__':
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
    
