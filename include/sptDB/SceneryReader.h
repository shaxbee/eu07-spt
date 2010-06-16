#ifndef SPTDB_SCENERYREADER_H
#define SPTDB_SCENERYREADER_H 1

#include <string>
#include <stack>
#include <vector>
#include <memory>
#include <fstream>
#include <boost/ptr_container/ptr_vector.hpp>

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

    template <typename T>
    void readOsgVec(T& output);

};

class SectorOffsetsReader
{
public:
    SectorOffsetsReader(std::ifstream& input);

    void readOffsets();
    bool hasSector(const osg::Vec2d& position);
    void getSectorOffset(const osg::Vec2d& position);

private:
    struct SectorOffset
    {
        osg::Vec2d position;
        size_t offset;
    };

    struct OffsetGreater;
    struct OffsetLess;

    typedef std::vector<SectorOffset> Offsets;
    Offsets _offsets;

    Offsets::const_iterator findSector(const osg::Vec2d& position);

    std::ifstream& _input;
    BinaryReader _reader;
};

class SectorReader
{

public:
    SectorReader(std::ifstream& input);
    std::auto_ptr<sptCore::Sector> readSector();

private:
    struct Header
    {
        unsigned int version;
    };

    typedef boost::ptr_vector<sptCore::RailTracking> Tracking;

    std::ifstream& _input;
    BinaryReader _reader;
    Tracking _tracking;

    std::auto_ptr<sptCore::Path> readPath();

    void readTracks(sptCore::DynamicSector& sector);
    void readSwitches(sptCore::DynamicSector& sector);
    void readNames();

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

template <typename T>
void BinaryReader::readOsgVec(T& output)
{
    assert_chunk_read(T::num_components * sizeof(typename T::value_type));
    _input.read(reinterpret_cast<char*>(output.ptr()), T::num_components * sizeof(typename T::value_type));
};

template <>
void BinaryReader::read(osg::Vec3f& output)
{
    readOsgVec(output);
};

template <>
void BinaryReader::read(osg::Vec3d& output)
{
    readOsgVec(output);
};

}; // namespace sptDB

#endif
