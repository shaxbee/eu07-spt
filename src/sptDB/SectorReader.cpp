#include "sptDB/SectorReader.h"

#include <string>
#include <vector>
#include <algorithm>

#include <boost/ptr_container/ptr_vector.hpp>

#include <sptCore/Scenery.h>
#include <sptCore/Sector.h>
#include <sptCore/Track.h>
#include <sptCore/SimpleTrack.h>
#include <sptCore/Switch.h>

#include <sptDB/BinaryReader.h>

#include <iostream>

using namespace boost;

using namespace sptCore;
using namespace sptDB;

namespace
{

enum PathType
{
    STRAIGHT = 0,
    BEZIER = 1
};

typedef boost::ptr_vector<SimpleTrack> SimpleTracks;
typedef boost::ptr_vector<Switch> Switches;

void print_vec(const osg::Vec3f& vec)
{
    std::cout << "(" << vec.x() << ", " << vec.y() << ", " << vec.z() << ") ";
}

std::auto_ptr<Path> readStraightPath(BinaryReader& reader)
{
//    std::cout << "STRAIGHT ";

    osg::Vec3f begin;
    osg::Vec3f end;

    reader.read(begin);
    reader.read(end);

//    print_vec(begin);
//    print_vec(end);

    return std::auto_ptr<Path>(new StraightPath(begin, end));
}

std::auto_ptr<Path> readBezierPath(BinaryReader& reader)
{
//    std::cout << "BEZIER ";

    osg::Vec3f begin;
    osg::Vec3f cpBegin;
    osg::Vec3f end;
    osg::Vec3f cpEnd;

    reader.read(begin);
    reader.read(cpBegin);
    reader.read(end);
    reader.read(cpEnd);

//    print_vec(begin);
//    print_vec(cpBegin);
//    print_vec(end);
//    print_vec(cpEnd);

    return std::auto_ptr<Path>(new BezierPath(begin, cpBegin, end, cpEnd));
};

std::auto_ptr<Path> readPath(BinaryReader& reader)
{
    uint8_t type;
    reader.read(type);

    if(type == STRAIGHT)
        return readStraightPath(reader);

    if(type == BEZIER)
        return readBezierPath(reader);

    assert(false && "Unsuported path type");

    return std::auto_ptr<Path>(NULL);
}; // ::readPath(reader)

osg::Vec3f readHeader(BinaryReader& reader)
{
    reader.expectChunk("HEAD");

    reader.expectVersion(Version(1, 2));
    osg::Vec3f result;
    reader.read(result);

    reader.endChunk("HEAD");

    return result;
}; // ::readHeader(reader)

void readTracks(osg::Vec3f sector, BinaryReader& reader, SimpleTracks& output)
{
    reader.expectChunk("TRLS");

    // straight tracks
    {
        uint32_t count;
        reader.read(count);

        while(count--)
        {
//            std::cout << "TRACK ";
            std::auto_ptr<Path> path = readStraightPath(reader);

            uint32_t front;
            reader.read(front);

            uint32_t back;
            reader.read(back);

            std::auto_ptr<SimpleTrack> track(new SimpleTrack(sector, path, TrackId(front), TrackId(back)));

            output.push_back(track);
//            std::cout << std::endl;
        };
    };

    // bezier tracks
    {
        uint32_t count;
        reader.read(count);

        while(count--)
        {
//            std::cout << "TRACK ";
            std::auto_ptr<Path> path = readBezierPath(reader);

            uint32_t front;
            reader.read(front);

            uint32_t back;
            reader.read(back);

            std::auto_ptr<SimpleTrack> track(new SimpleTrack(sector, path, TrackId(front), TrackId(back)));

            output.push_back(track);
//            std::cout << std::endl;
        };
    };

    reader.endChunk("TRLS");
}; // ::readTracks(sector, reader, output)

void readSwitches(const osg::Vec3f& sector, BinaryReader& reader, Switches& output)
{
    reader.expectChunk("SWLS");
    uint32_t count;
    reader.read(count);

    while(count--)
    {
//        std::cout << "SWITCH ";

        uint8_t position;
        reader.read(position);
        std::string position_str(position ? "DIVERTED" : "STRAIGHT");
//        std::cout << "POS_" << position_str << " ";

        std::auto_ptr<Switch> switch_(new Switch(
            sector, 
            readPath(reader), // straight
            readPath(reader), // diverted
            TrackId(reader.read<uint32_t>()), // commonId
            TrackId(reader.read<uint32_t>()), // straightId
            TrackId(reader.read<uint32_t>()), // divertedId,
            position_str));

        output.push_back(switch_);
//        std::cout << std::endl;
    };

    reader.endChunk("SWLS");
}; // ::readSwitches(sector, reader, output)

void readCustomTracking(Sector& sector, BinaryReader& reader, Tracks& tracks, Switches& switches)
{
    reader.expectChunk("RTLS");
    uint32_t count;
    reader.read(count);

    if(count != 0)
        throw std::logic_error("Custom Track reading not implemented");

    reader.endChunk("RTLS");
};

void readTrackNames(Scenery& scenery, BinaryReader& reader, SimpleTracks& tracks)
{
    reader.expectChunk("TRNM");
    uint32_t count;
    reader.read(count);

    while(count--)
    {
        uint32_t index;
        reader.read(index);

        std::string name;
        reader.read(name);

        std::cout << "TRACK " << index << " ALIAS " << name << std::endl;

        scenery.addTrack(name, tracks.at(index));
    };

    reader.endChunk("TRNM");
};

void readSwitchNames(Scenery& scenery, BinaryReader& reader, Switches& switches)
{
    // read named tracks
    {
        reader.expectChunk("SWNM");
        uint32_t count;
        reader.read(count);

        while(count--)
        {
            uint32_t index;
            reader.read(index);

            std::string name;
            reader.read(name);

            scenery.addSwitch(name, switches.at(index));
        };
        reader.endChunk("SWNM");
    };
}; // ::readSwitchNames

}; // anonymous namespace

namespace sptDB
{

#if 0
std::auto_ptr<Sector> readSector(std::ifstream& input, Scenery& scenery, const osg::Vec3d& position)
{
    SectorReaderCallback callback;
    readSector(input, scenery, position, callback);
};
#endif

osg::Vec3f readSector(std::istream& input, Scenery& scenery)
{
    BinaryReader reader(input);

    reader.expectChunk("SECT");

    osg::Vec3f position = readHeader(reader);

    // TRLS - Tracks List
    SimpleTracks simpleTracks;
    readTracks(position, reader, simpleTracks);

    // SWLS - Switches List
    Switches switches;
    readSwitches(position, reader, switches);

#if 0
    // RTLS - Custom Track List
    readCustomTracking(*sector, reader, tracks, switches);
#endif

    // TRNM - Track Names
    readTrackNames(scenery, reader, simpleTracks);

    // SWNM - Switch Names
    readSwitchNames(scenery, reader, switches);

    Tracks tracks;
    tracks.reserve(simpleTracks.size() + switches.size());
    tracks.transfer(tracks.begin(), simpleTracks);
    tracks.transfer(tracks.end() - 1, switches);

//    connections.insert(connections.end(), externals.begin(), externals.end());

    reader.endChunk("SECT");

    scenery.addSector(std::auto_ptr<Sector>(new Sector(position, tracks)));

    return position;

};

}; // namespace sptDB
