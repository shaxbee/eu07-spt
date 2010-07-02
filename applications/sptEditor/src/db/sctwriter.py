from struct import Struct
from sptmath import Vec3

class Chunk(object):
    def __init__(self, name, size = 0):
        self.name = name
        self.data = bytearray(size)

class BinaryWriter(object):
    uIntFormat = Struct("I")
    vec3fFormat = Struct("fff")
    vec3dFormat = Struct("ddd")

    def __init__(self, ifile):
        self.__input = ifile
        self.__chunks = list()
        self.__currentChunk = None

    def __writeChunkToFile(self):
        self.__input.write(self.__currentChunk.name)
        self.__input.write(uIntFormat.pack(len(self.__currentChunk.data)))
        self.__input.write(self.__currentChunk.data)

    def beginChunk(self, name):
        if len(name) != 4:
            raise ValueError("Invalid chunk identifier")

        self.__chunks.append((name, bytearray()))
        self.__currentChunk = self.__chunks[-1] 

    def endChunk(self, name):
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
        self.__currentChunk.expand(value)

    def writeString(self, value):
        self.writeUInt(len(value))
        self.write(value)

    def writeUInt(self, value):
        self.writeFmt(uIntFormat, value)

__trackFormats = [
    Struct("B 3f3f"), # straight
    Struct("B 3f3f3f3f") # bezier
]

__switchFormats = [
    Struct("B 3f3f 3f3f"), # straight, straight
    Struct("B 3f3f 3f3f3f3f"), # straight, bezier
    Struct("B 3f3f3f3f 3f3f"), # bezier, straight
    Struct("B 3f3f3f3f 3f3f3f3f") # bezier, bezier
]

class PathKind(object):
    STRAIGHT = 0
    BEZIER = 1

class StraightPath(object):
    kind = PathKind.STRAIGHT

    def __init__(p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __sub__(self, other):
        self.p1 -= other
        self.p2 -= other

    def to_tuple(self):
        return (self.p1, self.p2)

class BezierPath(object):
    kind = PathKind.BEZIER

    def __init__(p1, v1, p2, v2):
        self.p1 = p1
        self.v1 = v1
        self.p2 = p2
        self.v2 = v2

    def __sub__(self, other):
        self.p1 -= other
        self.v1 -= other
        self.p2 -= other
        self.v2 -= other

    def to_tuple(self):
        return (self.p1, self.v1, self.p2, self.v2)

def __tracksGen(tracks, offset):
    for track in tracks:
        yield (track.path - offset).to_tuple()

def __switchGen(switches, offset):
    for switch in switches:
        fmt = __switchFormats[switch.straight.kind + switch.diverted.kind * 2]
        yield (fmt, (switch.straight - offset).to_tuple() + \
                    (switch.diverted - offset).to_tuple() + \
                    (0 if switch.position == "STRAIGHT" else 1,))

class SectorWriter(BinaryWriter):
    def __init__(self, output, offset):
        BinaryWriter.__init__(self, output)
        self.__offset = offset
        self.__tracks = [list(), list()]

    def __writeTrackList(self):
        self.beginChunk("TRLS")
        for kind in range(2):
            size = len(self.__tracks[PathKind.STRAIGHT])
            self.writeUInt(size)
            self.writeArray(__trackFormats[kind], __tracksGen(self.__tracks[kind], self.__offset), size)
        self.endChunk("TRLS")

    def __writeSwitchList(self):
        self.writeUInt(len(self.__switches))
        self.writeVarArray(__switchGen(self.__switches))

    def write(self):
        self.beginChunk("SECT")
        self.__writeTrackList()
        self.endChunk("SECT")

    def addTrack(self, track):
        if not track.v1 and not track.v2:
            track.path = StraightPath(track.p1, track.p2)
        else:
            track.path = BezierPath(track.p1, track.v1, track.p2, track.v2)
        self.__tracks[track.path.kind].append(track)

if __name__ == "__main__":
    class Track(object):
        def __init__(self, p1, v1, v2, p2):
            self.p1 = p1
            self.v1 = v1
            self.v2 = v2
            self.p2 = p2

    output = file("test.sct", "w+")
    writer = SectorWriter(output, Vec3())
    writer.addTrack(Track(Vec3(), Vec3(), Vec3(), Vec3(100, 100, 0)))
    writer.write()

    output.close()
