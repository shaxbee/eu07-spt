import os.path

from sptmath import Vec3
from model.tracks import Track, Switch

from sctwriter import write_sector
from scvwriter import write_variant

#SECTOR_CENTER = Vec3(SECTOR_SIZE / 2, SECTOR_SIZE / 2, 0)

def exportScenery(path, trackings):
    sectors = __sort_trackings(trackings):
    
    for sector in sectors:
        sector_name = "%d_%d.sct" % (sector.position.x, sector.position.y)
        with file(os.path.join(path, sector_name), "w") as fout:
            writeSector(fout, sector.position, sector.tracks, sector.switches)
            
    with file(os.path.join(path, "default.scv"), "w") as fout:
        writeVariant(fout, 0, sectors)
    
class SectorData(object):
    def __init__(self, position):
        self.tracks = list()
        self.switches = list()
    
def __sortTrackings(trackings):
    """
    Sort trackings by sector and type.
    
    :param trackings: tracking objects list.
    :returns: list of SectorData objects.
    """
    
    sectors = dict()
    
    for tracking in trackings:
        position = Vec3(math.ceil(tracking.p1.x) / SECTOR_SIZE, math.ceil(tracking.p1.y) / SECTOR_SIZE, 0)
        #position += SECTOR_CENTER
        
        if position not in sectors:
            sectors[position] = SectorData(position)
            
        if(type(tracking) is Track):
            sectors[position].tracks.append(tracking)
        elif(type(tracking) is Switch):
            sectors[position].switches.append(tracking)
            
    return sectors.values()