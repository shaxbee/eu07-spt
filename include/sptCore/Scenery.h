#ifndef SPTCORE_SCENERY_H
#define SPTCORE_SCENERY_H 1

#include "TrackLocator.h"

#include <memory>
#include <stdexcept>
#include <vector>

#include <osg/Vec2f>
#include <osg/Vec3f>

namespace sptCore
{

class Sector;

class Track;
class SimpleTrack;
class SwitchableTracking;

class SceneryState;

struct SceneryException: public std::runtime_error
{
    SceneryException(const std::string message): std::runtime_error(message) { };
};

typedef std::vector<std::pair<std::string, TrackId>> Aliases;

class Scenery
{
public:
    Scenery();
    ~Scenery();

    const Sector& getSector(const osg::Vec2f& position) const;
    Sector& getSector(const osg::Vec2f& position);

    bool hasSector(const osg::Vec2f& position) const;

    const Track& getNextTrack(const Track& track, const osg::Vec3f& from) const;

    const SimpleTrack& getTrack(const std::string& name) const;
    const SwitchableTracking& getSwitch(const std::string& name) const;

    //! Add sector to scenery and manage its lifetime
    //! \throw SceneryException if Sector with same name exists
    void addSector(Sector&& sector);

    //! Register track aliases
    void addAliases(const osg::Vec2f& sector, Aliases&& aliases);

    //! Register external connections
    void addExternals(const osg::Vec2f& sector, std::vector<std::pair<osg::Vec3f, TrackId>>&& entries);

private:
    std::unique_ptr<SceneryState> _state;
}; // class sptCore::Scenery

} // namespace sptCore

#endif // headerguard
