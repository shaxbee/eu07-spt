from struct import Struct
from sptmath import Vec3

class BinaryWriter(object):
    uIntFormat = Struct("I")
    vec3fFormat = Struct("fff")
    vec3dFormat = Struct("ddd")

    def __init__(self, ifile):
        self.__input = ifile

    def writeArray(self, fmt, data, count):
        buf = bytearray(fmt.size * count)
        offset = 0
        for values in data:
            fmt.pack_into(buf, offset, *values)
            offset += fmt.size
        self.__input.write(buf)

    def writeVarArray(self, data, size):
        buf = bytearray(size)
        offset = 0
        for fmt, values in data:
            fmt.pack_into(buf, offset, *values)
            offset += fmt.size
        self.__input.write(buf)

    def writeFmt(self, fmt, values):
        self.__input.writer(fmt.pack(*values))

    def writeChunk(self, name, data):
        self.__input.write(name)
        self.writeUInt(len(data))
        self.writeString(data)

    def writeString(self, value):
        self.writeUInt(len(value))
        self.__input.write(value)

    def writeUInt(self, value):
        self.writeFmt(uIntFormat, value)

__trackFormats = [
    Struct("B 3f3f"), # straight
    Struct("B 3f3f3f3f") # bezier
]

__switchFormats = [
    Struct("B 3f3f 3f3f B"), # straight, straight
    Struct("B 3f3f 3f3f3f3f B"), # straight, bezier
    Struct("B 3f3f3f3f 3f3f B"), # bezier, straight
    Struct("B 3f3f3f3f 3f3f3f3f B") # bezier, bezier
]

def pathToTuple(path, offset):
    if path is StraightPath:
        return (path.p1 - offset).to_tuple() + (path.p2 - offset).to_tuple()
    elif path is BezierPath:
        return (path.p1 - offset).to_tuple() + (path.v1 - offset).to_tuple() + \
               (path.p2 - offset).to_tuple() + (path.v2 - offset).to_tuple()

def __tracksGen(tracks, offset):
    for track in tracks:
        yield pathToTuple(track.path, offset)

def __switchGen(switches, offset):
    for switch in switches:
        fmt = __switchFormats[switch.straight.kind + switch.diverted.kind * 2]
        yield (fmt, pathToTuple(switch.straight, offset) + \
                    pathToTuple(switch.diverted, offset) + \
                    (0 if switch.position == "STRAIGHT" else 1,))

class SectorWriter(BinaryWriter):
    def __init__(self, ifile, offset):
        self.__init__(ifile)
        self.__offset = offset
        self.__tracks = [[], []]

    def __writeTrackList(self):
        for kind in range(2):
            size = len(self.__tracks[kind])
            self.writeUInt(size)
            self.writeArray(__trackFormats[kind], __tracksGen(self.__tracks[kind], self.__offset), size)

    def __writeSwitchList(self):
        self.writeUInt(len(self.data.switches))
        self.writeVarArray(__switchGen(self.__switches, self.__offset), self.__switchesSize);

    def addTrack(self, track):
        if track.path is StraightPath:
            self.__tracks[PathKind.STRAIGHT].append(track)
        elif track.path is BezierPath:
            self.__tracks[PathKind.BEZIER].append(track)
        elif track.path is ArcPath:
            self.__tracks[PathKind.ARC].append(_arcToBezier(track.path))
