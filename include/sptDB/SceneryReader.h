#ifndef SPTDB_SCENERYREADER_H
#define SPTDB_SCENERYREADER_H 1

namespace sptDB
{

class SceneryReader
{

public:
    SceneryReader(std::istream& stream): _input(stream) { }

private:
    template <typename T>
    void read(T& output);

    template <typename T>
    void read(std::vector<typename T>& output);

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

#ifdef DEBUG
    typedef std::pair<std::string, size_t> ChunkEntry;
    typedef std::stack<ChunkEntry> ChunkStack;
    ChunkIdStack _chunkStack;

    void checkChunkSize(size_t bytes);
    void pushChunk(std::string name, size_t size);
    void popChunk();
#endif

    typedef std::vector<unsigned int> SectorOffsets;
    SectorOffsets _sectorOffsets;

}; // class sptDB::SceneryReader

template <typename T>
SceneryReader::read(T& output)
{
    checkChunkSize(sizeof(T));
    _input.read(reinterpret_cast<char*>(&output), sizeof(T));
};

template <typename T>
SceneryReader::read(<std::vector<typename T>& output)
{
    unsigned int count;
    read(count);

    const unsigned int elementSize = sizeof(T);

    checkChunkSize(elementSize * count);
    assert(output.empty());

    output.reserve(count);

    while(count--)
    {
        T element;
        _input.read(reinterpret_cast<char*>(&element), elementSize);
        output.push_back(element);
    };
};

}; // namespace sptDB

#endif
