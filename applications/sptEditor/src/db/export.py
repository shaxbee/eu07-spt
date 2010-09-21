import math
import os.path

from sptmath import Vec3
from model.tracks import Track, Switch
from model.groups import RailContainer

from sctwriter import writeSector, SECTOR_SIZE
from scvwriter import writeVariant

#SECTOR_CENTER = Vec3(SECTOR_SIZE / 2, SECTOR_SIZE / 2, 0)

def exportScenery(path, trackings):
    sectors = dict()
    __sortTrackings(sectors, trackings)
        
    for sector in sectors.itervalues():
        print "exportScenery"
        print repr(sector.tracks)
        sector_name = "%+05d%+05d.sct" % (sector.position.x, sector.position.y)
        with file(os.path.abspath(os.path.join(path, sector_name)), "wb") as fout:
            writeSector(fout, sector.position, sector.tracks, sector.switches)
            
    with file(os.path.join(path, "default.scv"), "wb") as fout:
        writeVariant(fout, 0, sectors.values())
    
class SectorData(object):
    def __init__(self, position):
        self.position = position
        self.tracks = list()
        self.switches = list()
    
def __sortTrackings(sectors, trackings):
    """
    Sort trackings by sector and type.
    
    :param trackings: tracking objects list.
    :param sectors: dictionary of position -> sector
    :param target: name of sector target collection (tracks/switches)
    """
    
    for tracking in trackings:
        position = Vec3(math.floor(tracking.p1.x / SECTOR_SIZE), math.floor(tracking.p1.y / SECTOR_SIZE), 0)
        #position += SECTOR_CENTER
        
        if position not in sectors:
            sectors[position] = SectorData(position)
            
        if type(tracking) is Track:
            sectors[position].tracks.append(tracking)
        elif type(tracking) is Switch:
            sectors[position].switches.append(tracking)
        elif type(tracking) is RailContainer:
            print "RailContainer"
            __sortTrackings(sectors, tracking.tracks())
        
if __name__ == "__main__":
    import yaml
    import sptyaml
    
    sptyaml.configureYaml()
    scenery = yaml.load(file("../../../scenery/test", "r"))
    exportScenery("../../../scenery/test123", scenery.tracks.tracks())