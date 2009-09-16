#ifndef SPTCORE_SCENERY_H
#define SPTCORE_SCENERY_H 1

#include <string>
#include <boost/exception.hpp>

#include <osg/Vec3>

namespace sptCore
{

class Sector;
class Track;
class SwitchableTracking;
class EventedTrack;

class Scenery
{
public:
	virtual ~Scenery() { };

	virtual Sector& getSector(const osg::Vec3& position) const = 0;
    virtual bool hasSector(const osg::Vec3& position) const = 0;

	//! \throw UnknownRailTracking if tracking was not found
	virtual Track& getTrack(const std::string& name) const = 0;
	
	//! \throw UnknownRailTracking if tracking was not found	
	virtual SwitchableTracking& getSwitch(const std::string& name) const = 0;
	
	//! \throw UnknownRailTracking if tracking was not found	
//	virtual EventedTrack* getEventedTrack(const std::string& name) const = 0;
	
	typedef boost::error_info<struct tag_name, std::string> NameInfo;
	class UnknownRailTrackingException: public boost::exception { };
	
	typedef boost::error_info<struct tag_position, osg::Vec3> PositionInfo;
	class UnknownSectorException: public boost::exception { };

	struct Statistics
	{
		size_t sectors;
		size_t railTrackings;
		size_t tracks;
		size_t eventedTracks;
		size_t switches;
        size_t totalTracks;
	}; // struct sptCore::DynamicScenery::Statistics
	
	virtual const Statistics& getStatistics() const = 0;
	
}; // class sptCore::Scenery

} // namespace sptCore

#endif // headerguard
