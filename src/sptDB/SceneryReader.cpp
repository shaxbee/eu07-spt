#include "sptDB/SceneryReader.h"
#include "sptCore/DynamicSector.h"
#include "sptCore/Track.h"
#include "sptCore/Switch.h"

#include <algorithm>
#include <boost/ptr_container/ptr_vector.hpp>

using namespace sptDB;

namespace
{

enum PathType
{
    STRAIGHT = 0,
    BEZIER = 1
};

typedef boost::ptr_vector<sptCore::Track> Tracks;
typedef boost::ptr_vector<sptCore::Switch> Switches;

std::auto_ptr<sptCore::Path> readPath(BinaryReader& reader)
{
    char type;
    reader.read(type);
    
    if(type == STRAIGHT)
    {
        osg::Vec3f begin;
        osg::Vec3f end;

        reader.read(begin);
        reader.read(end);

        return std::auto_ptr<sptCore::Path>(new sptCore::StraightPath(begin, end));
    };

    if(type == BEZIER)
    {
        osg::Vec3f begin;
        osg::Vec3f cpBegin;
        osg::Vec3f end;
        osg::Vec3f cpEnd;

        reader.read(begin);
        reader.read(cpBegin);
        reader.read(end);
        reader.read(cpEnd);

        return std::auto_ptr<sptCore::Path>(new sptCore::BezierPath(begin, cpBegin, end, cpEnd));
    };

    assert(false && "Unsuported path type");
}; // ::readPath(reader)

void readTracks(sptCore::Sector& sector, BinaryReader& reader, Tracks& output)
{
    reader.expectChunk("TRLS");

    size_t count;
    reader.read(count);

    while(count--)
    {
        std::auto_ptr<sptCore::Path> path = readPath(reader);
        std::auto_ptr<sptCore::Track> track(new sptCore::Track(sector, path));
        output.push_back(track);
    };

    reader.endChunk("TRLS");
}; // ::readTracks(sector, reader, output)

void readSwitches(sptCore::Sector& sector, BinaryReader& reader, Switches& output)
{
    reader.expectChunk("SWLS");
    size_t count;
    reader.read(count);

    while(count--)
    {
        std::auto_ptr<sptCore::Path> straight = readPath(reader);
        std::auto_ptr<sptCore::Path> diverted = readPath(reader);
        std::auto_ptr<sptCore::Switch> switch_(new sptCore::Switch(sector, straight, diverted));
        output.push_back(switch_);
    };

    reader.endChunk("SWLS");
}; // ::readSwitches(sector, reader, output)

}; // anonymous namespace

struct SectorOffsetsReader::OffsetGreater
{
    bool operator()(const SectorOffset& left, const SectorOffset& right) { return right.position < left.position; }
};

struct SectorOffsetsReader::OffsetLess
{
    bool operator()(const SectorOffset& left, const SectorOffset& right) { return left.position < right.position; }
};

SectorReader::SectorReader(std::ifstream& input):
    _input(input), _reader(input)
{
};

void SectorOffsetsReader::readOffsets()
{
    assert(_reader.expectChunk("SROF"));
    _reader.read(_offsets);

    // check if offsets are sorted
    assert(std::adjacent_find(_offsets.begin(), _offsets.end(), OffsetGreater()) == _offsets.end() && "Invalid offsets order");
};

SectorOffsetsReader::Offsets::const_iterator SectorOffsetsReader::findSector(const osg::Vec2d& position)
{
    SectorOffset search = {position, 0};
    return std::lower_bound(_offsets.begin(), _offsets.end(), search, OffsetLess());
}

bool SectorOffsetsReader::hasSector(const osg::Vec2d& position)
{
    return findSector(position) != _offsets.end();
}

std::auto_ptr<sptCore::Sector> SectorReader::readSector()
{
    _reader.expectChunk("SECT");

    std::auto_ptr<sptCore::DynamicSector> sector;

    Tracks tracks;
    readTracks(*sector, _reader, tracks);

    Switches switches;
    readSwitches(*sector, _reader, switches);

    _reader.endChunk("SECT");

    return std::auto_ptr<sptCore::Sector>(sector);

};

void SectorReader::readNames()
{
    // read named tracks
    {
        _reader.expectChunk("TRNM");
        size_t count;
        _reader.read(count);

        while(count--)
        {

        };

        _reader.endChunk("TRNM");
    };

    // read named switches
    {
        _reader.expectChunk("SWNM");
        size_t count;
        _reader.read(count);

        while(count--)
        {

        };

        _reader.endChunk("SWNM");
    };
};
