#ifndef SECTOR_VIEW_H
#define SECTOR_VIEW_H 1

#include <osg/Geode>
#include <sptDB/SceneryReader.h>

class SectorViewBuilder: public sptDB::SectorReaderCallback
{
public:
    SectorViewBuilder(osg::Geode* target, osg::Geometry* profile): _target(target), _profile(profile) { };
    virtual ~SectorViewBuilder() { };

    virtual void visit(const sptCore::Track& tracking);
    virtual void visit(const sptCore::Switch& tracking);

private:
    osg::ref_ptr<osg::Geode> _target;
    osg::ref_ptr<osg::Geometry> _profile;

}; // SectorViewBuilder

#endif
