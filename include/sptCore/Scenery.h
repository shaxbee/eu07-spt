#ifndef SPTCORE_SCENERY_H
#define SPTCORE_SCENERY_H 1

#include <set>
#include <map>
#include <vector>

#include <memory>
#include <stdexcept>

#include <boost/ptr_container/ptr_map.hpp>
#include <boost/cstdint.hpp>
#include <boost/scoped_ptr.hpp>

#include <osg/Vec3d>

namespace sptCore
{

class Sector;

class Track;
class SwitchableTracking;
class Switch;

class ExternalsManager;

struct SceneryException: public std::runtime_error
{
    SceneryException(const std::string message): std::runtime_error(message) { };
};

class Scenery
{
public:
    Scenery();
    ~Scenery();

    const Sector& getSector(const osg::Vec3f& position) const;
    Sector& getSector(const osg::Vec3f& position);

    bool hasSector(const osg::Vec3f& position) const;

    Track& getTrack(const std::string& name);
    SwitchableTracking& getSwitch(const std::string& name);

//    const Statistics& getStatistics() const { return _statistics; };

    //! \brief Add sector to scenery and manage its lifetime
    //! \throw SceneryException if Sector with same name exists
    void addSector(std::auto_ptr<Sector> sector);

    //! \brief Remove sector from scenery and return ownership 
    //! \throw SceneryException if Sector with same name exists
    std::auto_ptr<Sector> removeSector(const osg::Vec3f& position);

    //! \brief Add named Track
    //! \throw SceneryException if Track with same name exists
    void addTrack(const std::string& name, Track& track);

    //! \brief Remove named Track
    //! \throw SceneryException when no Track with specified name is found
    void removeTrack(const std::string& name);

    //! \brief Add named SwitchableTracking
    //! \throw SceneryException if tracking with same name exists
    void addSwitch(const std::string& name, SwitchableTracking& track);

    //! \brief Remove named SwitchableTracking
    //! \throw SceneryException when no SwitchableTracking with specified name is found
    void removeSwitch(const std::string& name);

private:
    typedef boost::ptr_map<osg::Vec3f, Sector> Sectors;
    typedef std::map<std::string, Track*> Tracks;
    typedef std::map<std::string, SwitchableTracking*> Switches;

    boost::scoped_ptr<ExternalsManager> _externals;

    Sectors _sectors;
    Tracks _tracks;
    Switches _switches;

//    Statistics _statistics;

}; // class sptCore::Scenery

} // namespace sptCore

#endif // headerguard
