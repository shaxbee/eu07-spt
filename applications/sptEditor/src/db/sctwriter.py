import time

import array
import struct 
import operator

from struct import Struct
from sptmath import Vec3

from binwriter import BinaryWriter

SECTOR_SIZE = 1000

class SectorWriterError(RuntimeError):
    pass

class SectorWriter(BinaryWriter):
    def __init__(self, output, offset):
        BinaryWriter.__init__(self, output)
        self.__offset = offset
        self.__tracks = list()
        self.__tracksKinds = [array.array('f'), array.array('f')]
#        self.__tracksKinds = [list(), list()]
        self.__switches = list()

    def writeToFile(self):
        self.beginChunk("SECT")
        self.__buildTrackingIndex()
        self.__writeHeader()
        self.__writeTrackList()
        self.__writeSwitchList()
        self.__writeTrackNames()
        self.__writeSwitchNames()
        self.__writeConnections()
        self.endChunk("SECT")
        self.finalize()

    def addTrack(self, track):
        sectorTrack = SectorTrack(track, self.__offset)
        self.__tracks.append(sectorTrack)
        self.__tracksKinds[sectorTrack.path.kind].extend(sectorTrack.path.to_tuple())

    def addSwitch(self, switch):
        self.__switches.append(SectorSwitch(switch, self.__offset))

    def __writeHeader(self):
        self.beginChunk("HEAD")

        self.write(struct.pack("<3f", *self.__offset.to_tuple()))

        self.endChunk("HEAD")

    def __writeTrackList(self):
        self.beginChunk("TRLS")

        print "kinds: %d %d" % (len(self.__tracksKinds[0]), len(self.__tracksKinds[1]))

        for kind in range(0, 2):
            data = self.__tracksKinds[kind]
            self.writeUInt(len(data) / (6 if kind == PathKind.STRAIGHT else 12)) 
            self.write(struct.pack("<%df" % len(data), *data))

        self.endChunk("TRLS")

    def __writeSwitchList(self):
        self.beginChunk("SWLS")
        self.writeUInt(len(self.__switches))
        self.writeVarArray(_switchGen(self.__switches, self.__offset))
        self.endChunk("SWLS")

    def __collectNamedTracking(self, source):
        result = list()

        for tracking in source:
            if tracking.name is not None:
                result.append((self.__index[tracking], tracking.name))

        return result

    def __writeNames(self, source):
        self.writeUInt(len(source))

        for offset, name in source:
            self.writeUInt(offset)
            self.writeString(name)

    def __writeTrackNames(self):
        self.beginChunk("TRNM")
        tracks = self.__collectNamedTracking(self.__tracks)
        self.__writeNames(tracks)
        self.endChunk("TRNM")

    def __writeSwitchNames(self):
        self.beginChunk("SWNM")
        switches = self.__collectNamedTracking(self.__switches)
        self.__writeNames(switches)
        self.endChunk("SWNM")

    def __buildTrackingIndexImpl(self, source):
        offset = len(self.__index)

        for tracking in source:
            self.__index[tracking] = offset
            offset += 1

    def __buildTrackingIndex(self):
        self.__index = dict()
        self.__buildTrackingIndexImpl(self.__tracks)
        self.__buildTrackingIndexImpl(self.__switches)

    def __addConnection(self, position, left, right):
        if position.x < 0 or position.x > SECTOR_SIZE or position.y < 0 or position.y > SECTOR_SIZE:
            if position not in self.__externalConnections:
                self.__externalConnections[position] = self.__index[left]
        else:
            if position not in self.__internalConnections:
                self.__internalConnections[position] = (self.__index[left], self.__index[right])

    def __collectTracksConnections(self, source):
        self.__buildTrackingIndex()
        for track in source:
            if track.n1:
                self.__addConnection(track.p1, track, track.n1)
            if track.n2:
                self.__addConnection(track.p2, track, track.n2)

    def __collectConnections(self):
        self.__internalConnections = dict()
        self.__externalConnections = dict()

        for track in self.__tracks:
            if track.n1:
                self.__addConnection(track.p1, track, track.n1)
            if track.n2:
                self.__addConnection(track.p2, track, track.n2)

        for switch in self.__switches:
            if switch.n1:
                self.__addConnection(switch.p1, switch, switch.n1)
            if switch.n2:
                self.__addConnection(switch.p2, switch, switch.n2)
            if switch.n3:
                self.__addConnection(switch.p3, switch, switch.n3)

        self.__internalConnections = sorted(self.__internalConnections.iteritems(), key=operator.itemgetter(0))
        self.__externalConnections = sorted(self.__externalConnections.iteritems(), key=operator.itemgetter(0))

    def __writeConnections(self):
        self.beginChunk("CNLS")

        self.__collectConnections()

        self.writeUInt(len(self.__internalConnections))
        self.writeArray(
            _internalConnectionFormat, 
            (position.to_tuple() + indexes for position, indexes in self.__internalConnections),
            len(self.__internalConnections))

        self.writeUInt(len(self.__externalConnections))
        self.writeArray(
            _externalConnectionFormat, 
            (position.to_tuple() + (index, ) for position, index in self.__externalConnections),
            len(self.__externalConnections))

        self.endChunk("CNLS")

def _getPath(p1, v1, p2, v2):
    if v1 == p1 and v2 == p2:
        return StraightPath(p1, p2)
    
    return BezierPath(p1, v1, p2, v2)

def _translate(point, offset):
    return FastVec3(*(point - offset).to_tuple())

_trackFormats = [
    Struct("<3f3f"), # straight
    Struct("<3f3f3f3f") # bezier
]

_switchFormats = [
    Struct("<B B 3f3f B 3f3f"), # position, straight, straight
    Struct("<B B 3f3f B 3f3f3f3f"), # position, straight, bezier
    Struct("<B B 3f3f3f3f B 3f3f"), # position, bezier, straight
    Struct("<B B 3f3f3f3f B 3f3f3f3f") # position, bezier, bezier
]

_internalConnectionFormat = Struct("<3f I I") # position, from index, to index
_externalConnectionFormat = Struct("<3f I") # position, index

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
        p1 = _translate(source.p1, offset)
        v1 = _translate(source.v1, offset) + p1
        p2 = _translate(source.p2, offset)
        v2 = _translate(source.v2, offset) + p2

        self.path = _getPath(p1, v1, p2, v2)
        self.n1 = source.n1
        self.n2 = source.n2

        self.name = source.name

class SectorSwitch(object):
    def __init__(self, source, offset): 
        p1 = _translate(source.p1, offset)
        v1 = _translate(source.v1, offset) + p1 
        p2 = _translate(source.p2, offset)
        v2 = _translate(source.v2, offset) + p2
        p3 = _translate(source.p3, offset)
        v3 = _translate(source.v3, offset) + p3

        self.straight = _getPath(p1, v1, p2, v2)
        self.diverted = _getPath(p1, v1, p3, v3)

        self.n1 = source.n1
        self.n2 = source.n2
        self.n3 = source.n3

        self.name = source.name

def _tracksGen(tracks, offset):
    for track in tracks:
        yield track.path.to_tuple()

def _switchGen(switches, offset):
    for switch in switches:
        fmt = _switchFormats[switch.straight.kind + switch.diverted.kind * 2]
        yield (fmt, (0 if switch.position == "STRAIGHT" else 1,) + \
                    (switch.straight.kind,) + switch.straight.to_tuple() + \
                    (switch.diverted.kind,) + switch.diverted.to_tuple())

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

    output = file("test.sct", "w+")
    writer = SectorWriter(output, Vec3())

    zero = Vec3(0, 0, 0)

    tracks = [
         Track(zero, zero, Vec3(100, 1, 0), zero)]
#        Track(Vec3(100, 100, 0), Vec3(0, 100, 0), Vec3(200, 200, 0), Vec3(0, -100, 0), "start"),
#        Track(zero, Vec3(0, 100, 0), Vec3(100, 100, 0), Vec3(-100, 0, 0))]

#    tracks[0].connect(Vec3(100, 100, 0), tracks[1])

    for track in tracks:
        writer.addTrack(track)

    start = time.time()
    writer.writeToFile()
    writer.finalize()
    print "Time: %f ms" % ((time.time() - start) * 1000.0)
