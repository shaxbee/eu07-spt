#ifndef SPTDB_SCENERYREADER_H
#define SPTDB_SCENERYREADER_H 1

#include <memory>
#include <fstream>

#include <osg/Vec3d>

#include <sptCore/Sector.h>
#include <sptCore/Scenery.h>

#include <sptDB/BinaryReader.h>

namespace sptDB
{

class SectorReader
{

public:
    SectorReader(std::ifstream& input, sptCore::Scenery& scenery);
    std::auto_ptr<sptCore::Sector> readSector(const osg::Vec3d& position);

private:
    struct Header
    {
        unsigned int version;
    };

    std::ifstream& _input;
    sptCore::Scenery& _scenery;

    BinaryReader _reader;

}; // class sptDB::SceneryReader

}; // namespace sptDB

#endif
