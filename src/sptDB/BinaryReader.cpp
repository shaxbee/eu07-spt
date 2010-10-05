#include "sptDB/BinaryReader.h"

#include <boost/format.hpp>

using namespace boost;
using namespace sptDB;

void ChunkWatcher::check(uint32_t bytes)
{
    if(_chunks.empty())
        return;

    Chunk& chunk = _chunks.top();
    chunk.left -= bytes;

    if(chunk.left < 0)
        throw std::runtime_error(str(format("Unexpected end in chunk %s, tried to read %d bytes, %d bytes available") % chunk.name % bytes % (chunk.left + bytes)));
};

void ChunkWatcher::push(const std::string& name, uint32_t size)
{
    Chunk chunk = {name, size, size};
    _chunks.push(chunk);
};

void ChunkWatcher::pop(const std::string& name)
{
    Chunk& chunk = _chunks.top();

    if(name != chunk.name)
        throw std::logic_error(str(format("Invalid chunk end - got %s expected %s") % chunk.name % name));

    if(chunk.left != 0)
        throw std::runtime_error(str(format("Incomplete read of chunk %s, %d bytes left") % chunk.name % chunk.left));

    unsigned int size = chunk.size;
    _chunks.pop();

    if(!_chunks.empty())
    {
        _chunks.top().left -= size;
    }
};

const std::string& ChunkWatcher::current() const
{
	return _chunks.top().name;
};

bool Version::operator<(const Version& other) const
{
    return (major < other.major) || ((major == other.major) && (minor < other.minor));
};

bool Version::operator==(const Version& other) const
{
    return (major == other.major) && (minor == other.minor);
};

bool Version::operator>(const Version& other) const
{
    return (major > other.major) || ((major == other.major) && (minor > other.minor));
};

BinaryReader::BinaryReader(std::istream& stream): 
    _input(stream), _version(0xFF, 0xFF)
{ 
};

std::string BinaryReader::readChunk()
{
    char chunk[4];
    _watcher.check(4);
    _input.read(chunk, 4);

    uint32_t size;
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
    uint32_t length;
    read(length);

    char* buffer = new char[length];

    _watcher.check(length);
    _input.read(buffer, length);

    output = std::string(buffer, length);
    delete[] buffer;
};

void BinaryReader::readVersion()
{
    read(_version.major);
    read(_version.minor);
};

const Version& BinaryReader::getVersion() const
{
    if(_version.major == 0xFF && _version.minor == 0xFF)
        throw std::logic_error("Trying to access version before reading");
    
    return _version;
};
