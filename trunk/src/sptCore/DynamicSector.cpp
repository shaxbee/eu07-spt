#include <sptCore/DynamicSector.h>

using namespace sptCore;

RailTracking& DynamicSector::getNextTrack(const osg::Vec3& position, RailTracking* from)
{

    Connections::const_iterator iter = _connections.find(position);

    // if there was no connection at given position throw exception
    if(iter == _connections.end())
        throw UnknownConnectionException() << PositionInfo(position);

    assert(from == iter->second.first || from == iter->second.second);

    RailTracking* next = (iter->second.first == from ? iter->second.second : iter->second.first);

    // if connection doesn't have next tracking throw exception
    if(!next)
        throw  UnknownConnectionException() << PositionInfo(position);

    return *next;

}; // DynamicSector::getNextTrack

const Sector::Connection& DynamicSector::getConnection(const osg::Vec3& position)
{

    Connections::const_iterator iter = _connections.find(position);
    if(iter == _connections.end())
        throw UnknownConnectionException() << PositionInfo(position);

    return iter->second;

}; // DynamicSector::getConnection

void DynamicSector::addConnection(const osg::Vec3& position, RailTracking* track)
{

    Connections::iterator iter = _connections.find(position);

    // is there connection at given position?
    if(iter == _connections.end())
    {
        // create new connection with only one track connected
        _connections.insert(std::make_pair(position, std::make_pair(track, (RailTracking*) NULL)));
    }
    else
    {
        // if connection is full throw exception
        if(iter->second.first && iter->second.second)
            throw InvalidConnectionException() << PositionInfo(position);

        // set second track on connection
        iter->second.second = track;
    };

}; // DynamicSector::addConnection

void DynamicSector::addConnection(const osg::Vec3& position, RailTracking* left, RailTracking* right)
{

    std::pair<Connections::iterator, bool> ret = _connections.insert(std::make_pair(position, std::make_pair(left, right)));

    if(!ret.second)
        throw InvalidConnectionException() << PositionInfo(position);

}; // DynamicSector::addConnection

void DynamicSector::cleanup()
{

    Connections result;
    std::remove_copy_if(_connections.begin(), _connections.end(), std::inserter(result, result.end()), IsOrphaned());
    _connections.swap(result);

}; // DynamicSector::cleanup()
