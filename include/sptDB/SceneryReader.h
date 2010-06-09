#ifndef SPTDB_SCENERYREADER_H
#define SPTDB_SCENERYREADER_H 1

namespace sptDB
{

class SceneryReader
{

public:
    SceneryReader(std::istream& stream): _input(stream) { }

private:
    void readInt(int& output);
    void readUInt(unsigned int& output);
    void readFloat(float& output);
    void readChars(std::string& output, size_t count);
    void readString(std::string& output);
    template <typename T>
    void readVector(std::vector<typename T>& output);

    size_t readChunk(const std::string& type);

    void readHeader();
    void readSectorOffsets();
    void readSectorData(unsigned int id);

    struct Header
    {
        unsigned int dataSize;
        unsigned int version;
    };

    std::istream& _input;
    size_t _chunkBytesLeft;

    typedef std::vector<unsigned int> SectorOffsets;
    SectorOffsets _sectorOffsets;

}; // class sptDB::SceneryReader

template <typename T>
SceneryReader::readVector(<std::vector<typename T>& output)
{
    unsigned int size;
    readUInt(size);

    const unsigned int elementSize = sizeof(T);

    assert(elementSize * size < _chunkBytesLeft);
    assert(output.empty());

    output.reserve(size);

    while(size--)
    {
        T element;
        _input.read(reinterpret_cast<char*>(&element), elementSize);
        output.push_back(element);
    };
};

}; // namespace sptDB

#endif
