#ifndef SPTCORE_DYNAMICSCENERY_H
#define SPTCORE_DYNAMICSCENERY_H 1

#include <sptCore/Scenery.h>

#include <sptUtil/AutoMap.h>

namespace sptCore
{

class Sector;

class Track;
class Switch;

class DynamicScenery: public Scenery
{
public:
	virtual ~DynamicScenery() { };

	virtual Sector& getSector(const osg::Vec3& position) const;
    virtual bool hasSector(const osg::Vec3& position) const;

	virtual Track& getTrack(const std::string& name) const;
//	virtual EventedTrack& getEventedTrack(const std::string& name) const;
	virtual SwitchableTracking& getSwitch(const std::string& name) const;

	typedef sptUtil::AutoMap<osg::Vec3, Sector*> Sectors;
	typedef std::map<std::string, Track*> Tracks;
	typedef std::map<std::string, SwitchableTracking*> Switches;

    const Sectors& getSectors() const { return _sectors; }
    const Tracks& getTracks() const { return _tracks; }
    const Switches& getSwitches() const { return _switches; }

	virtual const Statistics& getStatistics() const { return _statistics; };

    //! \brief Add sector to scenery and manage its lifetime
	//! \throw SectorExistsException if Sector with same name exists
	void addSector(std::auto_ptr<Sector> sector);

    //! \brief Remove sector from scenery and return ownership 
	//! \throw SectorNotFoundException if Sector with same name exists
    std::auto_ptr<Sector> removeSector(const osg::Vec3& position);

    //! \brief Add named Track
	//! \throw RailTrackingExistsException if Track with same name exists
	void addTrack(const std::string& name, Track& track);

    //! \brief Remove named Track
    //! \throw RailTrackingNotFoundException when no Track with specified name is found
    void removeTrack(const std::string& name);

//	//! \throw RailTrackingExistsException if EventedTrack with same name exists
//	void addEventedTrack(const std::string& name, EventedTrack* track);

    //! \brief Add named SwitchableTracking
	//! \throw RailTrackingExistsException if tracking with same name exists
	void addSwitch(const std::string& name, SwitchableTracking& track);

    //! \brief Remove named SwitchableTracking
    //! \throw RailTrackingNotFoundException when no SwitchableTracking with specified name is found
    void removeSwitch(const std::string& name);

	class SectorExistsException: public boost::exception { };
    class SectorNotFoundException: public boost::exception { };

	class RailTrackingExistsException: public boost::exception { };
    class RailTrackingNotFoundException: public boost::exception { };

private:
//	typedef std::map<std::string, boost::shared_ptr<EventedTrack> > EventedTracks;
//	EventedTracks _eventedTracks;
	Sectors _sectors;
	Tracks _tracks;
	Switches _switches;

	Statistics _statistics;

}; // class sptCore::DynamicScenery

} // namespace sptCore

#endif // headerguard
