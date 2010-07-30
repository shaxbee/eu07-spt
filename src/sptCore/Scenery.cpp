#include <sptCore/Scenery.h>

#include <sptCore/Sector.h>
#include <sptCore/Track.h>
#include <sptCore/Switch.h>

using namespace sptCore;

const Sector& Scenery::getSector(const osg::Vec3d& position) const
{
    try
    {
        return _sectors.at(position);
    } 
    catch(boost::bad_ptr_container_operation&) 
    {
        throw SectorNotFoundException() << PositionInfo(position);
    }
}; // Scenery::getSector
        
bool Scenery::hasSector(const osg::Vec3d& position) const
{

    Sectors::const_iterator iter = _sectors.find(position);
    return (iter != _sectors.end());

}; // Scenery::hasSector

Track& Scenery::getTrack(const std::string& name)
{

    Tracks::const_iterator iter = _tracks.find(name);
    
    if(iter == _tracks.end())
        throw RailTrackingNotFoundException() << NameInfo(name);

    return *(iter->second);
    
}; // Scenery::getTrack

SwitchableTracking& Scenery::getSwitch(const std::string& name)
{

    Switches::const_iterator iter = _switches.find(name);

    if(iter == _switches.end())
        throw RailTrackingNotFoundException() << NameInfo(name);    

    return *(iter->second);
    
}; // Scenery::getSwitch

void Scenery::addSector(std::auto_ptr<Sector> sector)
{

//    size_t totalTracks = sector->getTracksCount();

    std::pair<Sectors::iterator, bool> ret;
    osg::Vec3f position(sector->getPosition());
    ret = _sectors.insert(position, sector);

    // if sector already existed
    if(!ret.second)
        throw SectorExistsException() << PositionInfo(sector->getPosition());

    // update statistics
//    _statistics.sectors++;
//    _statistics.totalTracks += totalTracks;
    
}; // Scenery::addSector

std::auto_ptr<Sector> Scenery::removeSector(const osg::Vec3d& position)
{

    Sectors::iterator iter = _sectors.find(position);

    if(iter == _sectors.end())
        throw SectorNotFoundException() << PositionInfo(position);

//    _statistics.totalTracks -= iter->second->getTracksCount();
//    _statistics.sectors--;

    return std::auto_ptr<Sector>(_sectors.release(iter).release());

}; // Scenery::removeSector

void Scenery::addTrack(const std::string& name, Track& track)
{
    
    std::pair<Tracks::iterator, bool> ret;
    ret = _tracks.insert(std::make_pair(name, &track));
    
    if(!ret.second)
        throw RailTrackingExistsException() << NameInfo(name);

//    _statistics.tracks++;
    
}; // Scenery::addTrack

void Scenery::removeTrack(const std::string& name)
{

    Tracks::iterator iter = _tracks.find(name);

    if(iter != _tracks.end())
    {
//        _statistics.tracks--;
        _tracks.erase(iter);
    };

}; // Scenery::removeTrack

void Scenery::addSwitch(const std::string& name, SwitchableTracking& track)
{
    
    std::pair<Switches::iterator, bool> ret;
    ret = _switches.insert(std::make_pair(name, &track));
    
    if(!ret.second)
        throw RailTrackingExistsException() << NameInfo(name);

//    _statistics.switches++;
    
}; // Scenery::addSwitch

void Scenery::removeSwitch(const std::string& name)
{

    Switches::iterator iter = _switches.find(name);

    if(iter != _switches.end())
    {
//        _statistics.switches--;
        _switches.erase(iter);
    };

}; // Scenery::removeSwitch
