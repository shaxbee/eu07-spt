#include "sptDB/SectorReader.h"

#include <string>
#include <vector>
#include <algorithm>
#include <functional>

#include <sptCore/Scenery.h>
#include <sptCore/Sector.h>
#include <sptCore/Track.h>
#include <sptCore/SimpleTrack.h>
#include <sptCore/Switch.h>

#include <sptDB/BinaryReader.h>

#include <iostream>

using namespace std::placeholders;

using namespace sptCore;
using namespace sptDB;

namespace
{

enum PathType
{
    STRAIGHT = 0,
    BEZIER = 1
};

typedef std::vector<std::pair<osg::Vec3f, TrackId>> Externals;
typedef std::vector<std::pair<std::string, TrackId>> Aliases;

void print_vec(const osg::Vec3f& vec)
{
    std::cout << "(" << vec.x() << ", " << vec.y() << ", " << vec.z() << ") ";
}

std::shared_ptr<Path> readStraightPath(BinaryReader& reader)
{
    osg::Vec3f begin;
    osg::Vec3f end;

    reader.read(begin);
    reader.read(end);

    return std::make_shared<StraightPath>(begin, end);
}

std::shared_ptr<Path> readBezierPath(BinaryReader& reader)
{
    osg::Vec3f begin;
    osg::Vec3f cpBegin;
    osg::Vec3f end;
    osg::Vec3f cpEnd;

    reader.read(begin);
    reader.read(cpBegin);
    reader.read(end);
    reader.read(cpEnd);

    return std::make_shared<BezierPath>(begin, cpBegin, end, cpEnd);
};

std::shared_ptr<Path> readPath(BinaryReader& reader)
{
    uint8_t type;
    reader.read(type);

    if(type == STRAIGHT)
        return readStraightPath(reader);

    if(type == BEZIER)
        return readBezierPath(reader);

    throw std::logic_error("Unsupported path type");    
}; // ::readPath(reader)

TrackId readId(BinaryReader& reader, const osg::Vec3f& position, TrackId current, Externals& externals)
{
    uint32_t id;
    reader.read(id);

    TrackId result(id);

    if(result.isExternal())
    {
        externals.push_back({position, current});
    };

    return result;
};    

osg::Vec2f readHeader(BinaryReader& reader)
{
    reader.expectChunk("HEAD");

    reader.expectVersion(Version(1, 3));

    osg::Vec2f offset;
    reader.read(offset);

    reader.endChunk("HEAD");

    return offset;
}; // ::readHeader(reader)

void readTracks(const osg::Vec2f& sector, BinaryReader& reader, Tracks& output, Externals& externals)
{
    reader.expectChunk("TRLS");

    uint32_t count;
    reader.read(count);

    while(count--)
    {
        auto _readId = std::bind(&readId, std::ref(reader), _1, TrackId(output.size()), std::ref(externals));
        auto path = readPath(reader);

        output.push_back(std::unique_ptr<Track>(new SimpleTrack(
            sector, 
            path, 
            _readId(path->front()),
            _readId(path->back())
        )));
    };

    reader.endChunk("TRLS");
}; // ::readTracks(sector, reader, output)

void readSwitches(const osg::Vec2f& sector, BinaryReader& reader, Tracks& output, Externals& externals)
{
    reader.expectChunk("SWLS");
    uint32_t count;
    reader.read(count);

    while(count--)
    {
        auto _readId = std::bind(&readId, std::ref(reader), _1, TrackId(output.size()), std::ref(externals));

        uint8_t position;
        reader.read(position);

        auto straight = readPath(reader);
        auto diverted = readPath(reader);

        output.push_back(std::unique_ptr<Track>(new Switch(
            sector, 
            straight,
            diverted,
            _readId(straight->front()),
            _readId(straight->back()),
            _readId(diverted->back()),
            position ? "DIVERTED" : "STRAIGHT"
        )));
    };

    reader.endChunk("SWLS");
}; // ::readSwitches(sector, reader, output)

void readCustomTracking(Sector& sector, BinaryReader& reader, Tracks& tracks)
{
    reader.expectChunk("RTLS");

    uint32_t count;
    reader.read(count);
    if(count != 0)
    {    
        throw std::logic_error("Custom Track reading not implemented");
    }    

    reader.endChunk("RTLS");
};

Aliases&& readAliases(BinaryReader& reader)
{
    Aliases result;

    reader.expectChunk("TRNM");
    uint32_t count;
    reader.read(count);
    
    while(count--)
    {
        uint32_t index;
        reader.read(index);

        std::string name;
        reader.read(name);

        result.push_back({name, TrackId(index)});
    };

    reader.endChunk("TRNM");

    return std::move(result);
};

}; // anonymous namespace

namespace sptDB
{

osg::Vec2f readSector(std::istream& input, Scenery& scenery)
{
    BinaryReader reader(input);

    reader.expectChunk("SECT");

    auto position = readHeader(reader);

    Tracks tracks;
    Externals externals;

    // TRLS - Tracks List
    readTracks(position, reader, tracks, externals);

    // SWLS - Switches List
    readSwitches(position, reader, tracks, externals);

#if 0
    // RTLS - Custom Track List
    readCustomTracking(*sector, reader, tracks, switches);
#endif

    // TRNM - Track Names
    auto aliases = readAliases(reader); 

    reader.endChunk("SECT");

    scenery.addSector(Sector(position, std::move(tracks)));
    scenery.addAliases(position, aliases);
    scenery.addExternals(position, externals);

    return position;
};

}; // namespace sptDB
