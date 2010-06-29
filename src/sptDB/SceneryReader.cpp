#include "sptDB/SceneryReader.h"

#include <string>
#include <algorithm>

#include <boost/ptr_container/ptr_vector.hpp>

#include <sptCore/Scenery.h>
#include <sptCore/Sector.h>
#include <sptCore/Track.h>
#include <sptCore/Switch.h>

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

void readTrackNames(sptCore::Scenery& scenery, BinaryReader& reader, Tracks& tracks)
{
    // read named tracks
    {
        reader.expectChunk("TRNM");
        size_t count;
        reader.read(count);

        while(count--)
        {
            int index;
            reader.read(index);

            std::string name;
            reader.read(name);

            scenery.addTrack(name, tracks.at(index));
        };

        reader.endChunk("TRNM");
    };
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

std::auto_ptr<sptCore::Sector> SectorReader::readSector()
{
    _reader.expectChunk("SECT");

    std::auto_ptr<sptCore::Sector> sector;

    Tracks tracks;
    readTracks(*sector, _reader, tracks);

    Switches switches;
    readSwitches(*sector, _reader, switches);

    readTrackNames(_scenery, _reader, tracks);
    readSwitchNames(_scenery, _reader, switches);

    _reader.endChunk("SECT");

    return sector;

};
