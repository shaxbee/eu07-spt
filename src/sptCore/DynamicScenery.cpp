#include <sptCore/DynamicScenery.h>

#include <sptCore/Sector.h>
#include <sptCore/Track.h>
#include <sptCore/Switch.h>

using namespace sptCore;

Sector& DynamicScenery::getSector(const osg::Vec3& position)
{

    try
    {
        return _sectors.at(position);
    } 
    catch(boost::bad_ptr_container_operation) 
    {
        throw SectorNotFoundException() << PositionInfo(position);
    }
    
}; // DynamicScenery::getSector
        
bool DynamicScenery::hasSector(const osg::Vec3& position) const
{

    Sectors::const_iterator iter = _sectors.find(position);
    return (iter != _sectors.end());

}; // DynamicScenery::hasSector

Track& DynamicScenery::getTrack(const std::string& name)
{

    Tracks::const_iterator iter = _tracks.find(name);
    
    if(iter == _tracks.end())
        throw RailTrackingNotFoundException() << NameInfo(name);

    return *(iter->second);
    
}; // DynamicScenery::getTrack

//EventedTrack* DynamicScenery::getEventedTrack(const std::string& name) const
//{
//    
//    return getValueFromMap<EventedTracks, UnknownRailTrackingException, NameInfo>(_eventedTracks, name);
//    
//}; // DynamicScenery::getEventedTrack

SwitchableTracking& DynamicScenery::getSwitch(const std::string& name)
{

    Switches::const_iterator iter = _switches.find(name);

    if(iter == _switches.end())
        throw RailTrackingNotFoundException() << NameInfo(name);    

    return *(iter->second);
    
}; // DynamicScenery::getSwitch

void DynamicScenery::addSector(std::auto_ptr<Sector> sector)
{

    size_t totalTracks = sector->getTotalTracks();

    std::pair<Sectors::iterator, bool> ret;
    osg::Vec3f position(sector->getPosition());
    ret = _sectors.insert(position, sector);

    // if sector already existed
    if(!ret.second)
        throw SectorExistsException() << PositionInfo(sector->getPosition());

    // update statistics
    _statistics.sectors++;
    _statistics.totalTracks += totalTracks;
    
}; // DynamicScenery::addSector

std::auto_ptr<Sector> DynamicScenery::removeSector(const osg::Vec3& position)
{

    Sectors::iterator iter = _sectors.find(position);

    if(iter == _sectors.end())
        throw SectorNotFoundException() << PositionInfo(position);

    _statistics.totalTracks -= iter->second->getTotalTracks();
    _statistics.sectors--;

    return std::auto_ptr<Sector>(_sectors.release(iter).release());

}; // DynamicScenery::removeSector

void DynamicScenery::addTrack(const std::string& name, Track& track)
{
    
    std::pair<Tracks::iterator, bool> ret;
    ret = _tracks.insert(std::make_pair(name, &track));
    
    if(!ret.second)
        throw RailTrackingExistsException() << NameInfo(name);

    _statistics.tracks++;
    
}; // DynamicScenery::addTrack

void DynamicScenery::removeTrack(const std::string& name)
{

    Tracks::iterator iter = _tracks.find(name);

    if(iter != _tracks.end())
    {
        _statistics.tracks--;
        _tracks.erase(iter);
    };

}; // DynamicScenery::removeTrack


//void DynamicScenery::addEventedTrack(const std::string& name, EventedTrack* track)
//{
//    
//    insertValueToMap<EventedTracks, RailTrackingExistsException, NameInfo>(_eventedTracks, name, track);
//    _statistics.eventedTracks++;
//    
//}; // DynamicScenery::addEventedTrack

void DynamicScenery::addSwitch(const std::string& name, SwitchableTracking& track)
{
    
    std::pair<Switches::iterator, bool> ret;
    ret = _switches.insert(std::make_pair(name, &track));
    
    if(!ret.second)
        throw RailTrackingExistsException() << NameInfo(name);

    _statistics.switches++;
    
}; // DynamicScenery::addSwitch

void DynamicScenery::removeSwitch(const std::string& name)
{

    Switches::iterator iter = _switches.find(name);

    if(iter != _switches.end())
    {
        _statistics.switches--;
        _switches.erase(iter);
    };

}; // DynamicScenery::removeSwitch
