#include <sptCore/DynamicSector.h>

using namespace sptCore;

RailTracking* DynamicSector::getNextTrack(const osg::Vec3& position, RailTracking* from) const
{

    Connections::const_iterator iter = _connections.find(position);
    if(iter == _connections.end() || (from != iter->second.first && from != iter->second.second))
        throw UnknownConnectionException() << PositionInfo(position);

    return (iter->second.first == from ? iter->second.second : iter->second.first);

}; // DynamicSector::getNextTrack

Sector::Connection DynamicSector::getConnection(const osg::Vec3& position) const
{

    Connections::const_iterator iter = _connections.find(position);
    if(iter == _connections.end())
        throw UnknownConnectionException() << PositionInfo(position);

    return iter->second;

}; // DynamicSector::getConnection


void DynamicSector::addTrack(RailTracking* track, const osg::Vec3& position)
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

}; // DynamicSector::addTrack

void DynamicSector::addConnection(RailTracking* left, RailTracking* right, const osg::Vec3& position)
{

    std::pair<Connections::iterator, bool> ret = _connections.insert(std::make_pair(position, std::make_pair(left, right)));

    if(!ret.second)
        throw InvalidConnectionException() << PositionInfo(position);

}; // DynamicSector::addConnection
