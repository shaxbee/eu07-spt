import struct

class BinaryWriter(object):
    uIntFormat = struct.Struct("I")
    vec3fFormat = struct.Struct("fff")
    vec3dFormat = struct.Struct("ddd")

    def __init__(self, ifile):
        self.__input = ifile

    def writeChunk(self, name, data):
        self.__input.write(name)
        self.writeUInt(len(data))
        self.writeString(data)

    def writeString(self, value):
        self.writeUInt(len(value))
        self.__input.write(value)

    def writeUInt(self, value):
        self.__input.write(BinaryWriter.uIntFormat.pack(value))

    def writeVec3f(self, value):
        self.__input.write(BinaryWriter.vec3fFormat.pack(value.x, value.y, value.z))

    def writeVec3d(self, value):
        self.__input.write(BinaryWriter.vec3dFormat.pack(value.x, value.y, value.z))

class SectorWriter(object):
    def __init__(self, ifile, data):
        self.__writer = BinaryWriter(ifile)

    def __writePath(self, path):
        self.writeUInt(path.kind)
        if path.kind == 0:
            self.writeVec3f(path.begin)
            self.writeVec3f(path.end)
        elif path.kind == 1:
            self.writeVec3f(path.begin)
            self.writeVec3f(path.beginCP)
            self.writeVec3f(path.end)
            self.writeVec3f(path.endCP)

    def __writeTrackList(self):
        self.writeUInt(len(self.data.tracks))
        for track in self.data.tracks:
            self.__writePath(track.path)

    def __writeSwitchList(self):
        self.writeUInt(len(self.data.switches))
        for switch in self.data.switches:
            self.__writePath(switch.straight)
            self.__writePath(switch.diverted)
            self.__writer.writeString(switch.position)
