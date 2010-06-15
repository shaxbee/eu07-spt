#include "sptDB/SceneryReader.h"
#include "sptCore/DynamicSector.h"

#include <algorithm>

using namespace sptDB;

namespace
{

enum PathType
{
    STRAIGHT = 0,
    BEZIER = 1
};

};

struct SectorsReader::SectorOffsetGreater
{
    bool operator()(const SectorOffset& left, const SectorOffset& right) { return right.position < left.position; }
};

struct SectorsReader::SectorOffsetLess
{
    bool operator()(const SectorOffset& left, const SectorOffset& right) { return left.position < right.position; }
};

SectorsReader::SectorsReader(std::ifstream& input):
    _input(input), _reader(input)
{
    _offset = input.tellg();
};

void SectorsReader::readOffsets()
{
    assert(_reader.expectChunk("SROF"));
    _reader.read(_sectorOffsets);

    // check if offsets are sorted
    assert(std::adjacent_find(_sectorOffsets.begin(), _sectorOffsets.end(), SectorOffsetGreater()) == _sectorOffsets.end());
};

SectorsReader::SectorOffsets::const_iterator SectorsReader::findSector(const osg::Vec2d& position)
{
    SectorOffset search = {position, 0};
    return std::lower_bound(_sectorOffsets.begin(), _sectorOffsets.end(), search, SectorOffsetLess());
}

bool SectorsReader::hasSector(const osg::Vec2d& position)
{
    return findSector(position) != _sectorOffsets.end();
}

std::auto_ptr<sptCore::Sector> SectorsReader::readSector(const osg::Vec2d& position)
{
    SectorOffsets::const_iterator iter = findSector(position);

    if(iter == _sectorOffsets.end())
        throw std::range_error("Trying to read non-existing sector");

    size_t prevOffset = _input.tellg();

    _input.seekg(_offset + iter->offset);
    _reader.expectChunk("SECT");

    std::auto_ptr<sptCore::DynamicSector> sector;

    readTracks(*sector);
    readSwitches(*sector);

    _reader.endChunk("SECT");
    _input.seekg(prevOffset);

    return std::auto_ptr<sptCore::Sector>(NULL);

};

std::auto_ptr<sptCore::Path> SectorsReader::readPath()
{
    char type;
    _reader.read(type);
    
    if(type == STRAIGHT)
    {
        osg::Vec3f begin;
        osg::Vec3f end;

        _reader.read(begin);
        _reader.read(end);

        return std::auto_ptr<sptCore::Path>(new sptCore::StraightPath(begin, end));
    };

    if(type == BEZIER)
    {
        osg::Vec3f begin;
        osg::Vec3f cpBegin;
        osg::Vec3f end;
        osg::Vec3f cpEnd;

        _reader.read(begin);
        _reader.read(cpBegin);
        _reader.read(end);
        _reader.read(cpEnd);

        return std::auto_ptr<sptCore::Path>(new sptCore::BezierPath(begin, cpBegin, end, cpEnd));
    };

    assert(false && "Unsuported path type");

};

void SectorsReader::readTracks(sptCore::DynamicSector& sector)
{
    _reader.expectChunk("TRLS");

    size_t count;
    _reader.read(count);

    while(count--)
    {
//        sector.addTrack(new sptCore::Track(readPath()));
    };

    _reader.endChunk("TRLS");
}

void SectorsReader::readSwitches(sptCore::DynamicSector& sector)
{
    _reader.expectChunk("SWLS");
    size_t count;
    _reader.read(count);

    while(count--)
    {

    };

    _reader.endChunk("SWLS");
}
