#ifndef SPTCORE_DYNAMICSCENERY_H
#define SPTCORE_DYNAMICSCENERY_H 1

#include <sptCore/Scenery.h>

#include <map>
#include <boost/shared_ptr.hpp>

namespace sptCore
{

class Sector;
class Track;
class Switch;
class EventedTrack;

class DynamicScenery: public Scenery
{
public:
	virtual ~DynamicScenery() { };

	virtual Sector* getSector(const osg::Vec3& position) const;

	virtual Track* getTrack(const std::string& name) const;
//	virtual EventedTrack* getEventedTrack(const std::string& name) const;	
	virtual Switch* getSwitch(const std::string& name) const;
	
	//! \throw SectorExistsException if Sector with same name exists	
	void addSector(Sector* sector);
	
	//! \throw RailTrackingExistsException if Track with same name exists
	void addTrack(const std::string& name, Track* track);
	
	//! \throw RailTrackingExistsException if EventedTrack with same name exists	
//	void addEventedTrack(const std::string& name, EventedTrack* track);
	
	//! \throw RailTrackingExistsException if Switch with same name exists	
	void addSwitch(const std::string& name, Switch* track);

	class SectorExistsException: public boost::exception { };
	class RailTrackingExistsException: public boost::exception { };
	
	struct Statistics
	{
		size_t sectors;
		size_t railTrackings;
		size_t tracks;
		size_t eventedTracks;
		size_t switches;
	}; // struct sptCore::DynamicScenery::Stastics
	
	const Statistics& getStatistics() const;
	
protected:
	typedef std::map<osg::Vec3, boost::shared_ptr<Sector> > Sectors;	

	typedef std::map<std::string, boost::shared_ptr<Track> > Tracks;
//s	typedef std::map<std::string, boost::shared_ptr<EventedTrack> > EventedTracks;
	typedef std::map<std::string, boost::shared_ptr<Switch> > Switches;

	Sectors _sectors;

	Tracks _tracks;
//	EventedTracks _eventedTracks;
	Switches _switches;

	Stastics _statistics;
		
}; // class sptCore::DynamicScenery

} // namespace sptCore

#endif // headerguard