#ifndef SPTDB_SCENERYREADER_H
#define SPTDB_SCENERYREADER_H 1

#include <string>
#include <stack>
#include <vector>
#include <memory>
#include <fstream>

#include "sptCore/DynamicSector.h"

namespace sptDB
{

#ifdef DEBUG
class ChunkWatcher
{

public:
    ChunkWatcher(std::ifstream& input);

    void check(size_t bytes);
    void push(const std::string& chunk, size_t size);
    void pop();

private:
    struct Chunk
    {
        const std::string& name;
        size_t size;
        size_t left;
    };

    typedef std::stack<Chunk> ChunkStack;
    ChunkStack _chunkStack;

    Chunk* _chunk;

    std::ifstream& input;

};
#endif

class BinaryReader
{
public:
    BinaryReader(std::ifstream& stream): _input(stream), _watcher(stream) { }

    template <typename T>
    void read(T& output);

    template <typename T>
    void read(std::vector<T>& output);

    std::string& readChunk();
    bool expectChunk(const std::string& type);
    void endChunk(const std::string& type);

private:
    std::ifstream& _input;

#ifdef DEBUG
    ChunkWatcher _watcher;
#endif

};

class SectorsReader
{

public:
    SectorsReader(std::ifstream& input);

    void readOffsets();

    bool hasSector(const osg::Vec2d& position);
    std::auto_ptr<sptCore::Sector> readSector(const osg::Vec2d& position);

private:
    struct Header
    {
        unsigned int version;
    };

    struct SectorOffset
    {
        osg::Vec2d position;
        size_t offset;
    };

    struct SectorOffsetGreater;
    struct SectorOffsetLess;

    std::ifstream& _input;
    BinaryReader _reader;

    typedef std::vector<SectorOffset> SectorOffsets;
    SectorOffsets _sectorOffsets;

    size_t _offset;

    SectorOffsets::const_iterator findSector(const osg::Vec2d& position);
    std::auto_ptr<sptCore::Sector> readSectorData(size_t offset);

    std::auto_ptr<sptCore::Path> readPath();
    void readTracks(sptCore::DynamicSector& sector);
    void readSwitches(sptCore::DynamicSector& sector);

}; // class sptDB::SceneryReader

#ifdef DEBUG
    #define assert_chunk_read(bytes) _watcher.check(bytes)
#else
    #define assert_chunk_read(ignore) ((void)0)
#endif

template <typename T>
void BinaryReader::read(T& output)
{
    assert_chunk_read(sizeof(T));
    _input.read(reinterpret_cast<char*>(&output), sizeof(T));
};

template <typename T>
void BinaryReader::read(std::vector<T>& output)
{
    size_t count;
    read(count);

    const unsigned int elementSize = sizeof(T);

    assert(output.empty() && "Trying to write to non-empty vector");
    assert_chunk_read(elementSize * count);

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
