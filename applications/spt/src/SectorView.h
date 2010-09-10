#ifndef SECTOR_VIEW_H
#define SECTOR_VIEW_H 1

#include <osg/Geode>
#include <sptDB/SceneryReader.h>

void createSectorGeometry(osg::Geode* target, osg::Geometry* profile, const sptCore::Sector& sector);

#endif
