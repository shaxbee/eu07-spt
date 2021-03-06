#ifndef SPTCORE_SCENERY_BUILDER_H
#define SPTCORE_SCENERY_BUILDER_H

#include <string>
#include <memory>

#include <osg/Vec3>

namespace sptCore
{

class Track;
class SimpleTrack;
class Switch;

class DynamicScenery;
class DynamicSector;

//! \brief Scenery construction Helper
//! Utility class that reduces complexity of creating working Scenery instance
//! \author Zbyszek "ShaXbee" Mandziejewicz
//! \date 16.09.2009
class SceneryBuilder
{

public:
    SceneryBuilder();
    SceneryBuilder(DynamicScenery* scenery);

    DynamicScenery& getScenery() { return *_scenery; }
    std::auto_ptr<DynamicScenery> releaseScenery() { return _scenery; }

    DynamicSector& getOrCreateSector(const osg::Vec3& position);

    DynamicSector& getCurrentSector() { return *_sector; }
    DynamicSector& setCurrentSector(const osg::Vec3& position);

    SimpleTrack& createTrack(const osg::Vec3& p1, const osg::Vec3& p2);
    SimpleTrack& createTrack(const osg::Vec3& p1, const osg::Vec3& cp1, const osg::Vec3& p2, const osg::Vec3& cp2);
    SimpleTrack& createTrack(const std::string& name, const osg::Vec3& p1, const osg::Vec3& p2);
    SimpleTrack& createTrack(const std::string& name, const osg::Vec3& p1, const osg::Vec3& cp1, const osg::Vec3& p2, const osg::Vec3& cp2);

    void removeTrack(SimpleTrack& track);
    void removeTrack(const std::string& name);

    Switch& createSwitch(const osg::Vec3& p1, const osg::Vec3& cp1, const osg::Vec3& p2, const osg::Vec3& cp2, const osg::Vec3& p3, const osg::Vec3& cp3);
    Switch& createSwitch(const std::string& name, const osg::Vec3& p1, const osg::Vec3& cp1, const osg::Vec3& p2, const osg::Vec3& cp2, const osg::Vec3& p3, const osg::Vec3& cp3);

    void removeSwitch(Switch& track);
    void removeSwitch(const std::string& name);

    void cleanup();

private:
    std::auto_ptr<DynamicScenery> _scenery;
    DynamicSector* _sector;

    void addConnection(const osg::Vec3& position, const Track& track);
    DynamicSector& createSector(const osg::Vec3& position);

}; // class sptCore::SceneryBuilder

} // namespace sptCore

#endif // header guard
