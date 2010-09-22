import math
import os.path

from sptmath import Vec3
from model.tracks import Track, Switch
from model.groups import RailContainer

from sctwriter import writeSector, SECTOR_SIZE
from scvwriter import writeVariant

#SECTOR_CENTER = Vec3(SECTOR_SIZE / 2, SECTOR_SIZE / 2, 0)

def exportScenery(path, tracks, switches, callback):
    sectors = dict()
    
    __sortTrackings(sectors, tracks, 'tracks')
    __sortTrackings(sectors, switches, 'switches')
    
    progress = 0
    percent = 0
    callback(percent);
        
    for sector in sectors.itervalues():
        print "exportScenery"
        print repr(sector.tracks)
        sector_name = "%+05d%+05d.sct" % (sector.position.x, sector.position.y)
        with file(os.path.abspath(os.path.join(path, sector_name)), "wb") as fout:
            writeSector(fout, sector.position, sector.tracks, sector.switches)
        
        progress += 1
        newPercent = (progress * 100) / len(sectors)
        if(newPercent > percent):
            percent = newPercent
            callback(percent)
            
    with file(os.path.join(path, "default.scv"), "wb") as fout:
        writeVariant(fout, 0, sectors.values())
    
class SectorData(object):
    def __init__(self, position, variant = 0):
        self.position = position
        self.tracks = list()
        self.switches = list()
        self.variant = variant
    
def __sortTrackings(sectors, trackings, dest):
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
            
        getattr(sectors[position], dest).append(tracking)            
        
if __name__ == "__main__":
    import yaml
    import sptyaml
    
    sptyaml.configureYaml()
    scenery = yaml.load(file("../../../scenery/test", "r"))
    exportScenery("../../../scenery/test123", scenery.tracks.tracks())