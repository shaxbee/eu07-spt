from struct import Struct
from sptmath import Vec3

class Chunk(object):
    def __init__(self, name, size = 0):
        self.name = name
        self.data = bytearray(size)

class BinaryWriter(object):
    uIntFormat = Struct("<I")
    vec3fFormat = Struct("<fff")
    vec3dFormat = Struct("<ddd")

    def __init__(self, ifile):
        self.__input = ifile
        self.__chunks = list()
        self.__currentChunk = None

    def __writeChunkToFile(self):
        print "write chunk %s %d" % (self.__currentChunk.name, len(self.__currentChunk.data))
        self.__input.write(self.__currentChunk.name)
        self.__input.write(BinaryWriter.uIntFormat.pack(len(self.__currentChunk.data)))
        self.__input.write(str(self.__currentChunk.data))

    def beginChunk(self, name):
        if len(name) != 4:
            raise ValueError("Invalid chunk identifier")

        self.__chunks.append(Chunk(name))
        self.__currentChunk = self.__chunks[-1] 

    def endChunk(self, name):
        print "end chunk %s %d" % (name, len(self.__currentChunk.data))
        if not len(self.__chunks):
            raise ValueError("No chunk to finish")
        if name != self.__currentChunk.name:
            raise ValueError("Incorrect chunk name")

        if len(self.__chunks) == 1:
            self.__writeChunkToFile()
        else:
            current = self.__currentChunk
            self.__currentChunk = self.__chunks[-2]
            self.write(current.name)
            self.writeString(current.data)
    
        self.__chunks.pop()

    def writeArray(self, fmt, data, count):
        buf = bytearray(fmt.size * count)
        offset = 0
        for values in data:
            fmt.pack_into(buf, offset, *values)
            offset += fmt.size
        self.write(buf)

    def writeVarArray(self, data):
        for fmt, values in data:
            self.write(fmt.pack(*values))

    def writeFmt(self, fmt, values):
        self.write(fmt.pack(*values))

    def write(self, value):
        self.__currentChunk.data.extend(value)

    def writeString(self, value):
        self.writeUInt(len(value))
        self.write(value)

    def writeUInt(self, value):
        self.write(BinaryWriter.uIntFormat.pack(value))

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

class PathKind(object):
    STRAIGHT = 0
    BEZIER = 1

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

def _tracksGen(tracks, offset):
    for track in tracks:
        yield track.path.to_tuple()

def _switchGen(switches, offset):
    for switch in switches:
        fmt = _switchFormats[switch.straight.kind + switch.diverted.kind * 2]
        yield (fmt, (0 if switch.position == "STRAIGHT" else 1,) + \
                    (switch.straight.kind,) + switch.straight.to_tuple() + \
                    (switch.diverted.kind,) + switch.diverted.to_tuple())

class SectorWriterError(RuntimeError):
    pass

class SectorWriter(BinaryWriter):
    def __init__(self, output, offset):
        BinaryWriter.__init__(self, output)
        self.__offset = offset
        self.__tracks = [list(), list()]
        self.__switches = list()

    def __writeTrackList(self):
        self.beginChunk("TRLS")
        for kind in range(2):
            self.writeUInt(len(self.__tracks[kind]))
            self.writeArray(_trackFormats[kind], _tracksGen(self.__tracks[kind], self.__offset), len(self.__tracks[kind]))
        self.endChunk("TRLS")

    def __writeSwitchList(self):
        self.beginChunk("SWLS")
        self.writeUInt(len(self.__switches))
        self.writeVarArray(_switchGen(self.__switches, self.__offset))
        self.endChunk("SWLS")

    def __collectNamedTracking(self, source, offset = 0):
        result = list()

        for tracking in source:
            if tracking.name:
                result.append((offset, tracking.name))
            offset += 1

        return result

    def __writeNames(self, source):
        self.writeUInt(len(source))

        for offset, name in source:
            self.writeUInt(offset)
            self.writeString(name)

    def __writeTrackNames(self):
        self.beginChunk("TRNM")
        tracks = self.__collectNamedTracking(self.__tracks[PathKind.STRAIGHT])
        tracks.extend(self.__collectNamedTracking(self.__tracks[PathKind.BEZIER], len(self.__tracks[PathKind.STRAIGHT])))
        self.__writeNames(tracks)
        self.endChunk("TRNM")

    def __writeSwitchNames(self):
        self.beginChunk("SWNM")
        switches = self.__collectNamedTracking(self.__switches)
        self.__writeNames(switches)
        self.endChunk("SWNM")

    def __buildTrackingIndexImpl(self, source, offset = 0):
        index = dict()
        for tracking in source:
            index[tracking] = offset
            offset += 1

        return index

    def __buildTrackingIndex(self):
        self.__index = self.__buildTrackingIndexImpl(self.__tracks)
        self.__index.extend(self.__buildTrackingIndexImpl(self.__switches, len(self.__tracks)))

    def __addInternalConnection(self, position, from, to):
        if position not in self.__connections:
            self.__connections[position] = (self.__index[from], self.__index[to])

    def __collectConnections(self):
        self.__connections = dict()

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

    def writeToFile(self):
        self.beginChunk("SECT")
        self.__writeTrackList()
        self.__writeSwitchList()
        self.__writeTrackNames()
        self.__writeSwitchNames()
        self.endChunk("SECT")

    def __getPath(self, p1, v1, p2, v2):
        if not v1 and not v2:
            return StraightPath(p1, p2)
        
        return BezierPath(p1, v1, p2, v2)

    def addTrack(self, track):
        track.p1 -= offset
        track.p2 -= offset

        track.path = self.__getPath(track.p1, track.v1, track.p2, track.v2)

        self.__tracks[track.path.kind].append(track)

    def addSwitch(self, switch):
        switch.p1 -= offset
        switch.p2 -= offset
        switch.p3 -= offset

        switch.straight = self.__getPath(switch.p1, switch.v1, switch.p2, switch.v2)
        switch.diverted = self.__getPath(switch.p1, switch.v1, switch.p3, switch.v3)

        self.__switches.append(switch)

if __name__ == "__main__":
    class Track(object):
        def __init__(self, path, name = None):
            self.path = path
            self.name = name

    class Switch(object):
        def __init__(self, straight, diverted, position = "STRAIGHT", name = None):
            self.straight = straight
            self.diverted = diverted
            self.position = position
            self.name = name

    output = file("test.sct", "w+")
    writer = SectorWriter(output, Vec3())
    writer.addTrack(Track(StraightPath(Vec3(100, 100, 0), Vec3(200, 100, 0)), "start"))
    writer.addTrack(Track(BezierPath(Vec3(), Vec3(), Vec3(), Vec3(100, 100, 0))))
    writer.addSwitch(Switch(StraightPath(Vec3(0, 0, 0), Vec3(100, 0, 0)), StraightPath(Vec3(0, 0, 0), Vec3(0, 100, 0))))
    writer.writeToFile()

    output.close()
