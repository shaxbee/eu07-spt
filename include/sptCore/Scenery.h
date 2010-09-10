#ifndef SPTCORE_SCENERY_H
#define SPTCORE_SCENERY_H 1

#include <map>
#include <memory>
#include <stdexcept>

#include <boost/ptr_container/ptr_map.hpp>

#include <osg/Vec3d>

namespace sptCore
{

class Sector;

class Track;
class SwitchableTracking;
class Switch;

struct SceneryException: public std::runtime_error
{
    SceneryException(const std::string message): std::runtime_error(message) { };
};

class Scenery
{
public:
    ~Scenery() { };

    const Sector& getSector(const osg::Vec3d& position) const;
    bool hasSector(const osg::Vec3d& position) const;

    Track& getTrack(const std::string& name);
//    EventedTrack& getEventedTrack(const std::string& name) const;
    SwitchableTracking& getSwitch(const std::string& name);

//    const Statistics& getStatistics() const { return _statistics; };

    //! \brief Add sector to scenery and manage its lifetime
    //! \throw SceneryException if Sector with same name exists
    void addSector(std::auto_ptr<Sector> sector);

    //! \brief Remove sector from scenery and return ownership 
    //! \throw SceneryException if Sector with same name exists
    std::auto_ptr<Sector> removeSector(const osg::Vec3d& position);

    //! \brief Add named Track
    //! \throw SceneryException if Track with same name exists
    void addTrack(const std::string& name, Track& track);

    //! \brief Remove named Track
    //! \throw SceneryException when no Track with specified name is found
    void removeTrack(const std::string& name);

//    //! \throw RailTrackingExistsException if EventedTrack with same name exists
//    void addEventedTrack(const std::string& name, EventedTrack* track);

    //! \brief Add named SwitchableTracking
    //! \throw SceneryException if tracking with same name exists
    void addSwitch(const std::string& name, SwitchableTracking& track);

    //! \brief Remove named SwitchableTracking
    //! \throw SceneryException when no SwitchableTracking with specified name is found
    void removeSwitch(const std::string& name);

private:
    typedef boost::ptr_map<osg::Vec3d, Sector> Sectors;
    typedef std::map<std::string, Track*> Tracks;
    typedef std::map<std::string, SwitchableTracking*> Switches;

//    typedef std::map<std::string, boost::shared_ptr<EventedTrack> > EventedTracks;
//    EventedTracks _eventedTracks;
    Sectors _sectors;
    Tracks _tracks;
    Switches _switches;

//    Statistics _statistics;

}; // class sptCore::Scenery

} // namespace sptCore

#endif // headerguard
