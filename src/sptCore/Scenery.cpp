#include <sptCore/Scenery.h>

#include <sptCore/Sector.h>
#include <sptCore/Track.h>
#include <sptCore/Switch.h>

#include <functional>
#include <boost/format.hpp>

using namespace boost;

namespace
{

static osg::Vec3f tolerance(0.001f, 0.001f, 0.001f);

struct ExternalConnectionOrdering: public std::binary_function<sptCore::ExternalConnection, sptCore::ExternalConnection, bool>
{
    result_type operator()(first_argument_type const& lhs, second_argument_type const& rhs) const
    {
        osg::Vec3f diff = lhs.offset - rhs.offset + lhs.position - rhs.position;
        return diff < -tolerance;
    };
};

};

namespace sptCore
{

class ExternalsManager
{
public:
    ExternalsManager(Scenery& scenery);
    ~ExternalsManager();
    
    void addExternals(Sector& sector);
    void removeExternals(const Sector& sector);

private:
    typedef std::multiset<ExternalConnection, ExternalConnectionOrdering> ExternalConnectionsSet;
    Scenery& _scenery;
    ExternalConnectionsSet _externals;
}; // class sptCore::ExternalsManager

ExternalsManager::ExternalsManager(Scenery& scenery): 
    _scenery(scenery)
{
};

ExternalsManager::~ExternalsManager() { };
    
void ExternalsManager::addExternals(Sector& sector)
{
    const ExternalConnections& externals = sector.getExternals();
    for(ExternalConnections::const_iterator iter = externals.begin(); iter != externals.end(); iter++)
    {
        ExternalConnectionsSet::const_iterator match = _externals.find(*iter);
        if(match != _externals.end())
        {
            const RailTracking* other = _scenery.getSector(match->offset).updateConnection(match->position, NULL, &sector.getRailTracking(match->index));
            sector.updateConnection(iter->position, NULL, other);
        };
    };

    _externals.insert(externals.begin(), externals.end());
};

void ExternalsManager::removeExternals(const Sector& sector)
{
    osg::Vec3f offset = sector.getPosition();
    for(ExternalConnectionsSet::iterator iter = _externals.begin(); iter != _externals.end(); iter++)
    {
        if(iter->offset == offset)
        {
            ExternalConnectionsSet::iterator current = iter;
            iter++;
            _externals.erase(current);
        }
        else
        {
            _scenery.getSector(iter->offset).updateConnection(iter->position, &sector.getRailTracking(iter->index), NULL);
        }
    };
};

Scenery::Scenery():
    _externals(new ExternalsManager(*this))
{
};

Scenery::~Scenery() { };

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

    _externals->addExternals(*sector);
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

    _externals->removeExternals(*iter->second);

//    _statistics.totalTracks -= iter->second->getTracksCount();
//    _statistics.sectors--;

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

}; // namespace sptCore
