#ifndef SPTDB_SCENERYREADER_H
#define SPTDB_SCENERYREADER_H 1

#include <memory>
#include <iostream>

#include <osg/Vec3d>

#include <sptCore/Sector.h>
#include <sptCore/Scenery.h>

namespace sptDB
{

//std::auto_ptr<sptCore::Sector> readSector(std::ifstream& input, sptCore::Scenery& scenery, const osg::Vec3d& position);
sptCore::Sector& readSector(std::istream& input, sptCore::Scenery& scenery);

}; // namespace sptDB

#endif
