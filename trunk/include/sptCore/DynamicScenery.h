#ifndef SPTCORE_DYNAMICSCENERY_H
#define SPTCORE_DYNAMICSCENERY_H 1

#include <sptCore/Scenery.h>

#include <map>

namespace sptCore
{

class Sector;

class Track;
class Switch;

class DynamicScenery: public Scenery
{
public:
	virtual ~DynamicScenery();

	virtual Sector& getSector(const osg::Vec3& position) const;

	virtual Track& getTrack(const std::string& name) const;
//	virtual EventedTrack& getEventedTrack(const std::string& name) const;
	virtual SwitchableTracking& getSwitch(const std::string& name) const;

	virtual const Statistics& getStatistics() const { return _statistics; };

    //! \brief Add sector to scenery and manage its lifetime
	//! \throw SectorExistsException if Sector with same name exists
	void addSector(Sector* sector);

    //! \brief Add named Track
	//! \throw RailTrackingExistsException if Track with same name exists
	void addTrack(const std::string& name, Track* track);

    //! \brief Remove named Track
    //! \throw UnknownRailTrackingException when no Track with specified name is found
//    void removeTrack(const std::string& name);

//	//! \throw RailTrackingExistsException if EventedTrack with same name exists
//	void addEventedTrack(const std::string& name, EventedTrack* track);

    //! \brief Add named SwitchableTracking
	//! \throw RailTrackingExistsException if tracking with same name exists
	void addSwitch(const std::string& name, SwitchableTracking* track);

	//! \brief Removed orphaned connections
	//! Search for connections with only one Track and remove them
	void cleanup();

	class SectorExistsException: public boost::exception { };
	class RailTrackingExistsException: public boost::exception { };

protected:
	typedef std::map<osg::Vec3, Sector*> Sectors;

	typedef std::map<std::string, Track*> Tracks;
//	typedef std::map<std::string, boost::shared_ptr<EventedTrack> > EventedTracks;
	typedef std::map<std::string, SwitchableTracking*> Switches;

	Sectors _sectors;

	Tracks _tracks;
//	EventedTracks _eventedTracks;
	Switches _switches;

	Statistics _statistics;

}; // class sptCore::DynamicScenery

} // namespace sptCore

#endif // headerguard
