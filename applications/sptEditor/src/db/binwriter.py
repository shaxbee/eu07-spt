from struct import Struct

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
        print "chunk %s %d" % (name, len(self.__currentChunk.data))
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

    def finalize(self):
        self.__input.close()
