#include "sptDB/BinaryReader.h"

#include <boost/format.hpp>

using boost::str, boost::format;

using namespace sptDB;

ChunkWatcher::ChunkWatcher(std::ifstream& input):
    _input(input)
{
};

void ChunkWatcher::check(size_t bytes)
{
    Chunk& chunk = _chunks.top();
    chunk.left -= bytes;

    if(chunk.left < 0)
        throw std::runtime_error(str(format("Unexpected chunk end, tried to read %d bytes, %d bytes available" % bytes % (chunk.left + bytes))));
};

void ChunkWatcher::push(const std::string& chunk, size_t size)
{
    Chunk chunk = {chunk, size, size};
    _chunks.push(chunk);
};

void ChunkWatcher::pop(const std::string& chunk)
{
    if(chunk != _chunks.top().name)
        throw std::logic_error(str(format("Invalid chunk end - got %s expected %s") % _chunks.top().name % chunk));

    if(_chunks.top().left != 0)
        throw std::runtime_error(str(format("Chunk read incomplete - %d bytes left) % _chunks.top().left));

    _chunks.pop();
};

BinaryReader::BinaryReader(std::ifstream& stream): 
    _input(stream), _watcher(stream) 
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
};

bool BinaryReader::expectChunk(const std::string& type)
{
    return readChunk() == type;
};

void BinaryReader::endChunk(const std::string& type)
{
    _watcher.pop(type);
};
