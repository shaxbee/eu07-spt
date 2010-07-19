#include "sptDB/BinaryReader.h"

#include <boost/format.hpp>

using namespace boost;
using namespace sptDB;

void ChunkWatcher::check(size_t bytes)
{
    if(_chunks.empty())
        return;

    Chunk& chunk = _chunks.top();
    chunk.left -= bytes;

    if(chunk.left < 0)
        throw std::runtime_error(str(format("Unexpected chunk end, tried to read %d bytes, %d bytes available") % bytes % (chunk.left + bytes)));
};

void ChunkWatcher::push(const std::string& name, size_t size)
{
    Chunk chunk = {name, size, size};
    _chunks.push(chunk);
};

void ChunkWatcher::pop(const std::string& name)
{
    if(name != _chunks.top().name)
        throw std::logic_error(str(format("Invalid chunk end - got %s expected %s") % _chunks.top().name % name));

    if(_chunks.top().left != 0)
        throw std::runtime_error(str(format("Chunk read incomplete - %d bytes left") % _chunks.top().left));

    _chunks.pop();
};

BinaryReader::BinaryReader(std::ifstream& stream): 
    _input(stream)
{ 
    _input.exceptions(std::ios::badbit | std::ios::failbit | std::ios::eofbit);
};

std::string BinaryReader::readChunk()
{
    char chunk[4];
    assert_chunk_read(4);
    _input.read(chunk, 4);

    size_t size;
    read(size);

    std::string name(chunk, 4);
    _watcher.push(name, size);

    return name;
};

bool BinaryReader::expectChunk(const std::string& type)
{
    return readChunk() == type;
};

void BinaryReader::endChunk(const std::string& type)
{
    _watcher.pop(type);
};

void BinaryReader::read(osg::Vec3f& output)
{
    readOsgVec(output);
};

void BinaryReader::read(osg::Vec3d& output)
{
    readOsgVec(output);
};

void BinaryReader::read(std::string& output)
{
    size_t length;
    read(length);

    char* buffer = new char[length];

    assert_chunk_read(length);
    _input.read(buffer, length);

    output = std::string(buffer, length);
    delete[] buffer;
};
