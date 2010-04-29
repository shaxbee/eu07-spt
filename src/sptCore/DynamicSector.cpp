#include <sptCore/DynamicSector.h>

#include <map>
#include <boost/ptr_container/ptr_set.hpp>

using namespace sptCore;

namespace sptCore
{

class DynamicSectorImpl
{

public:

    typedef std::map<osg::Vec3, Sector::Connection> Connections;
    typedef boost::ptr_set<RailTracking> Tracks;

    Connections _connections;
    Tracks _tracks;

private:
    friend class DynamicSector;
    DynamicSectorImpl() { };

}; // DynamicSectorImpl

}; // namespace sptCore

struct IsOrphaned
{

    template <typename value_type>
    bool operator()(const value_type& entry) { return !entry.second.first || !entry.second.second; }

}; // struct IsOrphaned

DynamicSector::DynamicSector(Scenery& scenery, osg::Vec3 position):
    Sector(scenery, position), _impl(new DynamicSectorImpl())
{
}; // DynamicSector::DynamicSector

DynamicSector::~DynamicSector()
{
}; // DynamicSector::~DynamicSector

const RailTracking& DynamicSector::getNextTrack(const osg::Vec3& position, const RailTracking& from) const
{

    DynamicSectorImpl::Connections::const_iterator iter = _impl->_connections.find(position);

    // if there was no connection at given position throw exception
    if(iter == _impl->_connections.end())
        throw UnknownConnectionException() << PositionInfo(position);

    assert(&from == iter->second.first || &from == iter->second.second);

    const RailTracking* next = (iter->second.first == &from ? iter->second.second : iter->second.first);

    // if connection doesn't have next tracking throw exception
    if(!next)
        throw UnknownConnectionException() << PositionInfo(position);

    return *next;

}; // DynamicSector::getNextTrack

const Sector::Connection& DynamicSector::getConnection(const osg::Vec3& position) const
{

    DynamicSectorImpl::Connections::const_iterator iter = _impl->_connections.find(position);
    if(iter == _impl->_connections.end())
        throw UnknownConnectionException() << PositionInfo(position);

    return iter->second;

}; // DynamicSector::getConnection

size_t DynamicSector::getTotalTracks() const
{

    return _impl->_tracks.size();

}; // DynamicSector::getTotalTracks

void DynamicSector::addTrack(std::auto_ptr<RailTracking> track) 
{ 

    _impl->_tracks.insert(track); 

}; // DynamicSector::addTrack

void DynamicSector::removeTrack(RailTracking& track) 
{ 

    _impl->_tracks.erase(track); 

}; // DynamicSector::removeTrack

void DynamicSector::addConnection(const osg::Vec3& position, const RailTracking& track)
{

    DynamicSectorImpl::Connections::iterator iter = _impl->_connections.find(position);

    // is there connection at given position?
    if(iter == _impl->_connections.end())
    {
        // create new connection with only one track connected
        _impl->_connections.insert(std::make_pair(position, std::make_pair(&track, (const RailTracking*) NULL)));
    }
    else
    {
        // if connection is full throw exception
        if(iter->second.first && iter->second.second)
            throw InvalidConnectionException() << PositionInfo(position);

        // set second track on connection
        iter->second.second = &track;
    };

}; // DynamicSector::addConnection

void DynamicSector::addConnection(const osg::Vec3& position, const RailTracking& left, const RailTracking& right)
{

    std::pair<DynamicSectorImpl::Connections::iterator, bool> ret = _impl->_connections.insert(std::make_pair(position, std::make_pair(&left, &right)));

    if(!ret.second)
        throw InvalidConnectionException() << PositionInfo(position);

}; // DynamicSector::addConnection

void DynamicSector::removeConnection(const osg::Vec3& position) 
{ 

    _impl->_connections.erase(position); 

}; // DynamicSector::removeConnection

void DynamicSector::cleanup()
{

    DynamicSectorImpl::Connections result;
    std::remove_copy_if(_impl->_connections.begin(), _impl->_connections.end(), std::inserter(result, result.end()), IsOrphaned());
    _impl->_connections.swap(result);

}; // DynamicSector::cleanup()
