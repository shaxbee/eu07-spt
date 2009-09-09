#include <sptCore/DynamicScenery.h>

#include <sptCore/Sector.h>

using namespace sptCore;

template <typename MapT, typename ExceptionT, typename ErrorInfoT>
typename inline MapT::value_type::element_type getValueFromMap(MapT map, typename MapT::key_type key)
{
		
	typename MapT::iterator iter = map.find(key);
	
	if(iter == map.end())
		throw ExceptionT() << ErrorInfoT(key);
			
	return iter->second.get();
			
}; // template getValueFromMap

template <typename MapT, typename ExceptionT, typename ErrorInfoT>
typename inline void insertValueToMap(MapT map, typename MapT::key_type key, typename MapT::value_type value)
{
	
	std::pair<typename MapT::iterator, bool> ret;
	ret = map.insert(typename MapT::value_type(key, value));
	
	if(!ret.second)
		throw ExceptionT() << ErrorInfoT(key);
	
};

Sector* DynamicScenery::getSector(const osg::Vec3& position) const
{
	
	return getValueFromMap<Sectors, UnknownSectorException, PositionInfo>(_sectors, position);
	
}; // DynamicScenery::getSector
		
Track* DynamicScenery::getTrack(const std::string& name) const
{
	
	return getValueFromMap<Tracks, UnknownRailTrackingException, NameInfo>(_tracks, name);
	
}; // DynamicScenery::getTrack

//EventedTrack* DynamicScenery::getEventedTrack(const std::string& name) const
//{
//	
//	return getValueFromMap<EventedTracks, UnknownRailTrackingException, NameInfo>(_eventedTracks, name);
//	
//}; // DynamicScenery::getEventedTrack

Switch* DynamicScenery::getSwitch(const std::string& name) const
{
	
	return getValueFromMap<Switches, UnknownRailTrackingException, NameInfo>(_switches, name);
	
}; // DynamicScenery::getSwitch

void DynamicScenery::addSector(Sector* sector)
{
	
	insertValueToMap<Sectors, SectorExistsException, PositionInfo>(_sectors, sector->getPosition(), sector);
	_statistics.sectors++;
	_statistics.totalTracks += sector->getTotalTracks();
	
}; // DynamicScenery::addSector

void DynamicScenery::addTrack(const std::string& name, Track* track)
{
	
	insertValueToMap<Tracks, RailTrackingExistsException, NameInfo>(_tracks, name, track);
	_statistics.tracks++;
	
}; // DynamicScenery::addTrack

//void DynamicScenery::addEventedTrack(const std::string& name, EventedTrack* track)
//{
//	
//	insertValueToMap<EventedTracks, RailTrackingExistsException, NameInfo>(_eventedTracks, name, track);
//	_statistics.eventedTracks++;
//	
//}; // DynamicScenery::addEventedTrack

void DynamicScenery::addSwitch(const std::string& name, Switch* track)
{
	
	insertValueToMap<Switches, RailTrackingExistsException, NameInfo>(_switches, name, track);
	_statistics.switches++;
	
}; // DynamicScenery::addSwitch