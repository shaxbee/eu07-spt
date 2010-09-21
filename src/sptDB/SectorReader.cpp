#include "sptDB/SectorReader.h"

#include <string>
#include <vector>
#include <algorithm>

#include <boost/ptr_container/ptr_vector.hpp>

#include <sptCore/Scenery.h>
#include <sptCore/Sector.h>
#include <sptCore/Track.h>
#include <sptCore/Switch.h>

#include <sptDB/BinaryReader.h>

#include <iostream>

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
typedef boost::ptr_vector<sptCore::RailTracking> RailTrackings;
typedef std::vector<sptCore::Sector::Connection> Connections;

void print_vec(const osg::Vec3f& vec)
{
    std::cout << "(" << vec.x() << ", " << vec.y() << ", " << vec.z() << ") ";
}

std::auto_ptr<sptCore::Path> readStraightPath(BinaryReader& reader)
{
    std::cout << "STRAIGHT ";

    osg::Vec3f begin;
    osg::Vec3f end;

    reader.read(begin);
    reader.read(end);

    print_vec(begin);
    print_vec(end);

    return std::auto_ptr<sptCore::Path>(new sptCore::StraightPath(begin, end));
}

std::auto_ptr<sptCore::Path> readBezierPath(BinaryReader& reader)
{
    std::cout << "BEZIER ";

    osg::Vec3f begin;
    osg::Vec3f cpBegin;
    osg::Vec3f end;
    osg::Vec3f cpEnd;

    reader.read(begin);
    reader.read(cpBegin);
    reader.read(end);
    reader.read(cpEnd);

    print_vec(begin);
    print_vec(cpBegin);
    print_vec(end);
    print_vec(cpEnd);

    return std::auto_ptr<sptCore::Path>(new sptCore::BezierPath(begin, cpBegin, end, cpEnd));
};

std::auto_ptr<sptCore::Path> readPath(BinaryReader& reader)
{
    char type;
    reader.read(type);
    
    if(type == STRAIGHT)
        return readStraightPath(reader);

    if(type == BEZIER)
        return readBezierPath(reader);

    assert(false && "Unsuported path type");

    return std::auto_ptr<sptCore::Path>(NULL);
}; // ::readPath(reader)

osg::Vec3d readHeader(BinaryReader& reader)
{
    reader.expectChunk("HEAD");

    reader.readVersion();
    osg::Vec3f result;
    reader.read(result);

    reader.endChunk("HEAD");

    return result;
}; // ::readHeader(reader)

void readTracks(sptCore::Sector& sector, BinaryReader& reader, Tracks& output)
{
    reader.expectChunk("TRLS");

    // straight tracks
    {
        size_t count;
        reader.read(count);

        while(count--)
        {
            std::cout << "TRACK ";
            std::auto_ptr<sptCore::Path> path = readStraightPath(reader);
            std::auto_ptr<sptCore::Track> track(new sptCore::Track(sector, path));

            output.push_back(track);
            std::cout << std::endl;
        };
    };

    // bezier tracks
    {
        size_t count;
        reader.read(count);

        while(count--)
        {
            std::cout << "TRACK ";
            std::auto_ptr<sptCore::Path> path = readBezierPath(reader);
            std::auto_ptr<sptCore::Track> track(new sptCore::Track(sector, path));

            output.push_back(track);
            std::cout << std::endl;
        };
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
        std::cout << "SWITCH ";

        unsigned char position;
        reader.read(position);
        std::string position_str(position ? "DIVERTED" : "STRAIGHT");
        std::cout << "POS_" << position_str << " ";

        std::auto_ptr<sptCore::Path> straight = readPath(reader);
        std::auto_ptr<sptCore::Path> diverted = readPath(reader);

        std::auto_ptr<sptCore::Switch> switch_(new sptCore::Switch(sector, straight, diverted, position_str));

        output.push_back(switch_);
        std::cout << std::endl;
    };

    reader.endChunk("SWLS");
}; // ::readSwitches(sector, reader, output)

void readCustomTracking(sptCore::Sector& sector, BinaryReader& reader, Tracks& tracks, Switches& switches)
{
    reader.expectChunk("RTLS");
    size_t count;
    reader.read(count);

    if(count != 0)
        throw std::logic_error("Custom RailTracking reading not implemented");

    reader.endChunk("RTLS");
};

void readConnections(BinaryReader& reader, const RailTrackings& trackings, Connections& connections, Connections& externals)
{
    reader.expectChunk("CNLS");

    // read internal connections
    {
        size_t count;
        reader.read(count);

        while(count--)
        {
            osg::Vec3f position;
            reader.read(position);

            size_t left;
            reader.read(left);

            size_t right;
            reader.read(right);

            sptCore::Sector::Connection connection =
            {
                position,
                &trackings.at(left),
                &trackings.at(right)
            };

            connections.push_back(connection);

        };

    };

    // read external connections
    {
        size_t count;
        reader.read(count);

        while(count--)
        {
            osg::Vec3f position;
            reader.read(position);

            size_t index;
            reader.read(index);

            sptCore::Sector::Connection connection = 
            {
                position,
                &trackings.at(index),
                NULL
            };

            externals.push_back(connection);
        };
    };

    reader.endChunk("CNLS");
}; // ::readConnections(reader, trackings, output)

void readTrackNames(sptCore::Scenery& scenery, BinaryReader& reader, Tracks& tracks)
{
    reader.expectChunk("TRNM");
    size_t count;
    reader.read(count);

    while(count--)
    {
        size_t index;
        reader.read(index);

        std::string name;
        reader.read(name);

        std::cout << "TRACK " << index << " ALIAS " << name << std::endl;

        scenery.addTrack(name, tracks.at(index));
    };

    reader.endChunk("TRNM");
};

void readSwitchNames(sptCore::Scenery& scenery, BinaryReader& reader, Switches& switches)
{
    // read named tracks
    {
        reader.expectChunk("SWNM");
        size_t count;
        reader.read(count);

        while(count--)
        {
            int index;
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
std::auto_ptr<sptCore::Sector> readSector(std::ifstream& input, sptCore::Scenery& scenery, const osg::Vec3d& position)
{
    SectorReaderCallback callback;
    readSector(input, scenery, position, callback);
};
#endif

sptCore::Sector& readSector(std::istream& input, sptCore::Scenery& scenery)
{
    BinaryReader reader(input);

    reader.expectChunk("SECT");

    osg::Vec3d position = readHeader(reader);
    std::auto_ptr<sptCore::Sector> sector(new sptCore::Sector(position));

    // TRLS - Tracks List
    Tracks tracks;
    readTracks(*sector, reader, tracks);

    // SWLS - Switches List
    Switches switches;
    readSwitches(*sector, reader, switches);

#if 0
    // RTLS - Custom RailTracking List
    readCustomTracking(*sector, reader, tracks, switches);
#endif

    // TRNM - Track Names
    readTrackNames(scenery, reader, tracks);

    // SWNM - Switch Names
    readSwitchNames(scenery, reader, switches);

    RailTrackings trackings;
    trackings.reserve(tracks.size() + switches.size());
    trackings.transfer(trackings.begin(), tracks);
    trackings.transfer(trackings.end() - 1, switches);

    // RTCN - RailTracking Connections
    Connections connections;
    Connections externals;
    readConnections(reader, trackings, connections, externals);

    sector->setData(trackings, connections);

    reader.endChunk("SECT");

    sptCore::Sector& sectorRef = *sector;
    scenery.addSector(sector);

    return sectorRef;

};

}; // namespace sptDB