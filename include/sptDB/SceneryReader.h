#ifndef SPTDB_SCENERYREADER_H
#define SPTDB_SCENERYREADER_H 1

#include <memory>
#include <fstream>

#include <osg/Vec3d>

#include <sptCore/Sector.h>
#include <sptCore/Scenery.h>

namespace sptDB
{

class SectorReaderCallback
{
public:
    virtual ~SectorReaderCallback() { };
    virtual void visit(const sptCore::Track& tracking) { };
    virtual void visit(const sptCore::Switch& tracking) { };
};

//std::auto_ptr<sptCore::Sector> readSector(std::ifstream& input, sptCore::Scenery& scenery, const osg::Vec3d& position);
std::auto_ptr<sptCore::Sector> readSector(std::ifstream& input, sptCore::Scenery& scenery, const osg::Vec3d& position, SectorReaderCallback callback = SectorReaderCallback());

}; // namespace sptDB

#endif
