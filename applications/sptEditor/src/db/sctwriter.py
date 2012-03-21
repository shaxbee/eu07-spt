import time

import array
import struct 
import operator
import itertools

from struct import Struct
from sptmath import Vec3, Decimal

from binwriter import BinaryWriter

SECTOR_SIZE = 2000
SECTOR_FILE_VERSION = "1.2"

MAX_UINT32 = 2 ** 32 - 1

class SectorWriteError(RuntimeError):
    pass
    
def writeSector(fout, position, tracks, switches):
    """
    Write sector data to file.
    
    :param fout: output file object.
    :param position: sector center position relative to scenery.
    :param tracks: list of tracks in sector.
    :param switches: list of switches in sector.
    :raises: SectorWriteError
    """
    writer = BinaryWriter(fout)
        
    # transform tracks and switches
    tracks = [SectorTrack(track, position) for track in tracks]
    switches = [SectorSwitch(switch, position) for switch in switches]
    
    # build id -> tracking index
    index = __buildTrackingIndex(tracks, switches)
    
    writer.beginChunk("SECT")
    
    __writeHeader(writer, position)
    
    __writeTrackList(writer, tracks, index)
    __writeSwitchList(writer, switches, index)
    
    __writeNames(writer, "TRNM", tracks, index)
    __writeNames(writer, "SWNM", switches, index)
    
    writer.endChunk("SECT")
    writer.finalize()
    
def __buildTrackingIndex(*args):
    index = dict()
    
    for source in args:
        # extract tracking.original
        keys = itertools.imap(operator.attrgetter('original'), source)
        # create list of ids
        values = range(len(index), len(index) + len(source) + 1)
        # update index with tracking.original -> id pairs
        
        index.update(itertools.izip(keys, values))        
            
    return index

def __connection(position, instance, index):
    if instance is None:
        return MAX_UINT32
    if (position.x < 0) or (position.x > SECTOR_SIZE) or (position.y < 0) or (position.y > SECTOR_SIZE):
        return MAX_UINT32 - 1
    return index[instance]
    
def __writeHeader(writer, position):
    writer.beginChunk("HEAD")
    
    writer.writeVersion(SECTOR_FILE_VERSION)
    # write sector position
    writer.writeFmt(Struct("<3f"), position.to_tuple())

    writer.endChunk("HEAD")
    
def __writeTrackList(writer, tracks, index):
    def writeKind(kind):
        fmt = __trackFormats[kind]
        source = [track.path.to_tuple() + (__connection(track.p1, track.n1, index), __connection(track.p2, track.n2, index)) for track in tracks if track.path.kind == kind]

        writer.writeUInt(len(source))
        for entry in source:
            writer.writeFmt(fmt, entry) 
        
    writer.beginChunk("TRLS")                
    writeKind(PathKind.STRAIGHT)
    writeKind(PathKind.BEZIER)
    writer.endChunk("TRLS")    
    
def __writeSwitchList(writer, switches, index):
    def flat(switch):
        fmt = __switchFormats[switch.straight.kind + switch.diverted.kind * 2]
        return (fmt, (0 if switch.position == "STRAIGHT" else 1,) + \
            (switch.straight.kind,) + switch.straight.to_tuple() + \
            (switch.diverted.kind,) + switch.diverted.to_tuple() + \
            (__connection(switch.pc, switch.nc, index), __connection(switch.p1, switch.n1, index), __connection(switch.p2, switch.n2, index)))
    
    writer.beginChunk("SWLS")
    writer.writeUInt(len(switches))
    writer.writeVarArray(itertools.imap(flat, switches))
    writer.endChunk("SWLS")
    
def __writeNames(writer, chunk, source, index):
    # create list of id -> name pairs for each named tracking
    source = [(index[tracking.original], tracking.name) for tracking in source if tracking.name is not None]

    writer.beginChunk(chunk)
        
    writer.writeUInt(len(source))
    for offset, name in source:
        writer.writeUInt(offset)
        writer.writeString(name)    
            
    writer.endChunk(chunk)
    
def _getPath(p1, v1, p2, v2):
    if v1 == p1 and v2 == p2:
        return StraightPath(p1, p2)
    
    return BezierPath(p1, v1, p2, v2)

def _translate(point, offset):
    return FastVec3(*(point - offset).to_tuple())

__trackFormats = [
    Struct("<3f3f I I"), # straight, prev track, next track
    Struct("<3f3f3f3f I I") # bezier, prev track, next track
]

__switchFormats = [
    Struct("<B B 3f3f B 3f3f I I I"), # position, straight, straight, common track, straight track, diverted track
    Struct("<B B 3f3f B 3f3f3f3f I I I"), # position, straight, bezier, common track, straight track, diverted track
    Struct("<B B 3f3f3f3f B 3f3f I I I"), # position, bezier, straight, common track, straight track, diverted track
    Struct("<B B 3f3f3f3f B 3f3f3f3f I I I") # position, bezier, bezier, common track, straight track, diverted track
]

class PathKind(object):
    STRAIGHT = 0
    BEZIER = 1

class FastVec3(object):
    def __init__(self, x = 0.0, y = 0.0, z = 0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, other):
        return FastVec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return FastVec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __eq__(self, other):
        return other != None and (abs(self.x - other.x) < 1e-6 and abs(self.y - other.y) < 1e-6 and abs(self.z - other.z) < 1e-6)
    
    @classmethod
    def from_vec3(cls, source):
        return FastVec3(source.x, source.y, source.z)

    def to_tuple(self):
        return (self.x, self.y, self.z)

    def __repr__(self):
        return "FastVec3(x = %.2f, y = %.2f, z = %.2f)" % self.to_tuple()
        
class StraightPath(object):
    kind = PathKind.STRAIGHT

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __sub__(self, other):
        return StraightPath(self.p1 - other, self.p2 - other)

    def to_tuple(self):
        return self.p1.to_tuple() + self.p2.to_tuple()
        
class BezierPath(object):
    kind = PathKind.BEZIER

    def __init__(self, p1, v1, p2, v2):
        self.p1 = p1
        self.v1 = v1
        self.p2 = p2
        self.v2 = v2

    def __sub__(self, other):
        return BezierPath(self.p1 - other, self.v1 - other, self.p2 - other, self.v2 - other)

    def to_tuple(self):
        return self.p1.to_tuple() + self.v1.to_tuple() + self.p2.to_tuple() + self.v2.to_tuple()

class SectorTrack(object):
    def __init__(self, source, offset): 
        self.p1 = _translate(source.p1, offset)
        self.v1 = self.p1 + FastVec3.from_vec3(source.v1)
        self.p2 = _translate(source.p2, offset)
        self.v2 = self.p2 + FastVec3.from_vec3(source.v2)

        self.path = _getPath(self.p1, self.v1, self.p2, self.v2)
        self.n1 = source.n1
        self.n2 = source.n2

        self.name = source.name
        self.original = source

class SectorSwitch(object):
    def __init__(self, source, offset): 
        self.pc = _translate(source.pc, offset)
        self.vc1 = self.pc + FastVec3.from_vec3(source.vc1)
        self.vc2 = self.pc + FastVec3.from_vec3(source.vc2)
        self.p1 = _translate(source.p1, offset)
        self.v1 = self.p1 + FastVec3.from_vec3(source.v1)
        self.p2 = _translate(source.p2, offset)
        self.v2 = self.p2 + FastVec3.from_vec3(source.v2)

        self.straight = _getPath(self.pc, self.vc1, self.p1, self.v1)
        self.diverted = _getPath(self.pc, self.vc2, self.p2, self.v2)

        self.nc = source.nc
        self.n1 = source.n1
        self.n2 = source.n2

        self.name = source.name
        self.position = "STRAIGHT"
        
        self.original = source

if __name__ == "__main__":
    class Track(object):
        def __init__(self, p1, v1, p2, v2, name = None):
            self.p1 = p1
            self.v1 = v1
            self.p2 = p2
            self.v2 = v2

            self.n1 = None
            self.n2 = None

            self.name = name

        def connect(self, point, tracking):
            if point == self.p1:
                self.n2 = tracking
            elif point == self.p2:
                self.n1 = tracking
            else:
                raise RuntimeError("Unknown point")

    class Switch(object):
        def __init__(self, p1, v1, p2, v2, p3, v3, position = "STRAIGHT", name = None):
            self.p1 = p1
            self.v1 = v1
            self.p2 = p2
            self.v2 = v2
            self.p3 = p3
            self.v3 = v3

            self.n1 = None
            self.n2 = None
            self.n3 = None

            self.position = position
            self.name = name

    zero = Vec3("0.0", "0.0", "0.0")

    tracks = [
         Track(zero, zero, Vec3("100.0", "1.0", "0.0"), zero)]
#        Track(Vec3(100, 100, 0), Vec3(0, 100, 0), Vec3(200, 200, 0), Vec3(0, -100, 0), "start"),
#        Track(zero, Vec3(0, 100, 0), Vec3(100, 100, 0), Vec3(-100, 0, 0))]

    switches = []

    start = time.time()
    writeSector(file("test.sct", "w+"), Vec3(), tracks, switches)
    print "Time: %f ms" % ((time.time() - start) * 1000.0)
