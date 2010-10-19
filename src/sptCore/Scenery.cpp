#include <sptCore/Scenery.h>

#include <sptCore/Sector.h>
#include <sptCore/Track.h>
#include <sptCore/Switch.h>

#include <boost/format.hpp>

using namespace sptCore;
using namespace boost;

ExternalsManager::ExternalsManager(Scenery& scenery): 
    _scenery(scenery)
{
};
    
void ExternalsManager::addExternals(const Sector& sector, const ExternalConnections& externals)
{
    for(ExternalConnections::const_iterator iter = externals.begin(); iter != externals.end(); iter++)
    {
        ExternalConnectionsSet::const_iterator match = _externals.find(*iter);
        if(match != _externals.end())
            _scenery.getSector(match->offset).updateConnection(match->position, NULL, &sector.getRailTracking(match->index));
    };

    _externals.insert(externals.begin(), externals.end());
};

void ExternalsManager::removeExternals(const osg::Vec3f& offset)
{
    for(ExternalConnectionsSet::iterator iter = _externals.begin(); iter != _externals.end(); iter++)
    {
        if(iter->offset == offset)
        {
            ExternalConnectionsSet::iterator current = iter;
            iter++;
            _externals.erase(current);
        }
    };
};

Sector& Scenery::getSector(const osg::Vec3f& position)
{
    try
    {
        return _sectors.at(position);
    } 
    catch(boost::bad_ptr_container_operation&) 
    {
        throw SceneryException(str(format("Sector already exists at position (%f, %f, %f)") %
                    position.x() %
                    position.y() %
                    position.z()));
    }
}; // Scenery::getSector

const Sector& Scenery::getSector(const osg::Vec3f& position) const
{
    try
    {
        return _sectors.at(position);
    } 
    catch(boost::bad_ptr_container_operation&) 
    {
        throw SceneryException(str(format("Sector already exists at position (%f, %f, %f)") %
                    position.x() %
                    position.y() %
                    position.z()));
    }
}; // Scenery::getSector
        
bool Scenery::hasSector(const osg::Vec3f& position) const
{
    Sectors::const_iterator iter = _sectors.find(position);
    return (iter != _sectors.end());
}; // Scenery::hasSector

Track& Scenery::getTrack(const std::string& name)
{
    Tracks::const_iterator iter = _tracks.find(name);
    
    if(iter == _tracks.end())
        throw SceneryException(str(format("Track with name %s doesn't exist.") % name));

    return *(iter->second);   
}; // Scenery::getTrack

SwitchableTracking& Scenery::getSwitch(const std::string& name)
{
    Switches::const_iterator iter = _switches.find(name);

    if(iter == _switches.end())
        throw SceneryException(str(format("Switch with name %s doesn't exist.") % name));

    return *(iter->second);   
}; // Scenery::getSwitch

void Scenery::addSector(std::auto_ptr<Sector> sector)
{
//    size_t totalTracks = sector->getTracksCount();
    osg::Vec3f position(sector->getPosition());
    Sectors::const_iterator iter = _sectors.find(position);

    if(iter != _sectors.end())
        throw SceneryException(str(format("Sector already exist at position (%f, %f, %f)") %
                    position.x() %
                    position.y() %
                    position.z()));

    registerExternalConnections(this, sector.get());
    _sectors.insert(position, sector);

    // update statistics
//    _statistics.sectors++;
//    _statistics.totalTracks += totalTracks;   
}; // Scenery::addSector

std::auto_ptr<Sector> Scenery::removeSector(const osg::Vec3f& position)
{
    Sectors::iterator iter = _sectors.find(position);

    if(iter == _sectors.end())
        throw SceneryException(str(format("No sector to remove at position (%f, %f, %f)") %
                    position.x() %
                    position.y() %
                    position.z()));

//    _statistics.totalTracks -= iter->second->getTracksCount();
//    _statistics.sectors--;

    unregisterExternalConnections(iter->second);

    return std::auto_ptr<Sector>(_sectors.release(iter).release());
}; // Scenery::removeSector

void Scenery::addTrack(const std::string& name, Track& track)
{
    std::pair<Tracks::iterator, bool> ret;
    ret = _tracks.insert(std::make_pair(name, &track));
    
    if(!ret.second)
        throw SceneryException(str(format("Track with name %s already exists.") % name));

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
        throw SceneryException(str(format("Switch with name %s already exists.") % name));

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
