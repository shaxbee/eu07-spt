import time

import array
import struct 
import operator
import itertools

from struct import Struct
from sptmath import Vec3

from binwriter import BinaryWriter

SECTOR_SIZE = 2000
SECTOR_FILE_VERSION = "1.1"

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
    
    print "sector position:", repr(position.to_tuple())
    
    # transform tracks and switches
    tracks = [SectorTrack(track, position) for track in tracks]
    switches = [SectorSwitch(switch, position) for switch in switches]
    
    # build id -> tracking index
    index = __buildTrackingIndex(tracks, switches)
    
    writer.beginChunk("SECT")
    
    __writeHeader(writer, position)
    
    __writeTrackList(writer, tracks)
    __writeSwitchList(writer, switches)
    
    __writeNames(writer, "TRNM", tracks, index)
    __writeNames(writer, "SWNM", switches, index)
    
    __writeConnections(writer, tracks, switches, index)
    
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
    
def __writeHeader(writer, position):
    writer.beginChunk("HEAD")
    
    writer.writeVersion(SECTOR_FILE_VERSION)
    # write sector position
    writer.writeFmt(Struct("<3f"), position.to_tuple())

    writer.endChunk("HEAD")
    
def __writeTrackList(writer, tracks):
    def writeKind(kind, recordSize):
        # get list of floats representing points of each track path
        source = list(track.path.to_tuple() for track in tracks if track.path.kind == kind)
            
        # write tracks count
        writer.writeUInt(len(source))
        # write points
        writer.writeArray(struct.Struct("<%df" % recordSize), source, len(source))
        
    writer.beginChunk("TRLS")                
    writeKind(PathKind.STRAIGHT, 6)
    writeKind(PathKind.BEZIER, 12)
    writer.endChunk("TRLS")    
    
def __writeSwitchList(writer, switches):
    def flat(switch):
        fmt = __switchFormats[switch.straight.kind + switch.diverted.kind * 2]
        return (fmt, (0 if switch.position == "STRAIGHT" else 1,) + \
            (switch.straight.kind,) + switch.straight.to_tuple() + \
            (switch.diverted.kind,) + switch.diverted.to_tuple())
    
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
    
def __collectConnections(tracks, switches, index):
    internal = dict()
    external = dict()       
        
    def addConnection(position, left, right):
        position = position.to_tuple()
        if (position[0] < 0) or (position[0] > SECTOR_SIZE) or (position[1] < 0) or (position[1] > SECTOR_SIZE):
            if position not in external:
                external[position] = index[left]
        else:
            if position not in internal:
                if right in index:
                    internal[position] = (index[left], index[right])
                else:
                    external[position] = index[left]
        
    for track in tracks:
        if track.n1 is not None:
            addConnection(track.p1, track.original, track.n1)
        if track.n2 is not None:
            addConnection(track.p2, track.original, track.n2)

    for switch in switches:
        if switch.nc is not None:
            addConnection(switch.pc, switch.original, switch.nc)
        if switch.n1 is not None:
            addConnection(switch.p1, switch.original, switch.n1)
        if switch.n2 is not None:
            addConnection(switch.p2, switch.original, switch.n2)
                
    # sort connections by position
    internal = sorted(internal.iteritems(), key=operator.itemgetter(0))
    external = sorted(external.iteritems(), key=operator.itemgetter(0))
        
    return (internal, external)

def __writeConnections(writer, tracks, switches, index):
    writer.beginChunk("CNLS")
        
    internal, external = __collectConnections(tracks, switches, index)

    writer.writeUInt(len(internal))
    writer.writeArray(Struct("<3f I I"), (position + indexes for position, indexes in internal), len(internal))

    writer.writeUInt(len(external))
    writer.writeArray(Struct("<3f I"), (position + (index, ) for position, index in external), len(external))

    writer.endChunk("CNLS")

def _getPath(p1, v1, p2, v2):
    if v1 == p1 and v2 == p2:
        return StraightPath(p1, p2)
    
    return BezierPath(p1, v1, p2, v2)

def _translate(point, offset):
    return FastVec3(*(point - offset).to_tuple())

__trackFormats = [
    Struct("<3f3f"), # straight
    Struct("<3f3f3f3f") # bezier
]

__switchFormats = [
    Struct("<B B 3f3f B 3f3f"), # position, straight, straight
    Struct("<B B 3f3f B 3f3f3f3f"), # position, straight, bezier
    Struct("<B B 3f3f3f3f B 3f3f"), # position, bezier, straight
    Struct("<B B 3f3f3f3f B 3f3f3f3f") # position, bezier, bezier
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

    zero = Vec3(0, 0, 0)

    tracks = [
         Track(zero, zero, Vec3(100, 1, 0), zero)]
#        Track(Vec3(100, 100, 0), Vec3(0, 100, 0), Vec3(200, 200, 0), Vec3(0, -100, 0), "start"),
#        Track(zero, Vec3(0, 100, 0), Vec3(100, 100, 0), Vec3(-100, 0, 0))]

    switches = []

    start = time.time()
    write_sector(file("test.sct", "w+"), Vec3(), tracks, switches)
    print "Time: %f ms" % ((time.time() - start) * 1000.0)
