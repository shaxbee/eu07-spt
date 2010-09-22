#include "sptCore/Sector.h"

using namespace sptCore;

float Sector::SIZE = 2000.0;

Sector::Sector(const osg::Vec3d& position): _position(position)
{

}; // Sector::Sector(scenery)

const RailTracking& Sector::getNextTrack(const osg::Vec3f& position, const RailTracking& from) const
{
    Connection search = {position, NULL, NULL};

    Connections::const_iterator iter = std::lower_bound(_connections.begin(), _connections.end(), search, ConnectionLess());

    if(iter->position != position || (iter->first != &from && iter->second != &from))
        throw UnknownConnectionException() << PositionInfo(position);

    const RailTracking* result = iter->first == &from ? iter->second : iter->first;

    if(!result)
        throw UnknownConnectionException() << PositionInfo(position);

    return *result;
}; // Sector::getNextTrack(position, from)

const RailTracking& Sector::getRailTracking(size_t index) const
{
    return _trackings.at(index);
};

size_t Sector::getRailTrackingCount() const
{
    return _trackings.size();
}; // Sector::getRailTrackingCount()

void Sector::updateConnection(const osg::Vec3f& position, const RailTracking* previous, const RailTracking* current)
{
    Connection search = {position, NULL, NULL};
    Connections::iterator iter = std::lower_bound(_connections.begin(), _connections.end(), search, ConnectionLess());

    if(iter->position != position)
        throw UnknownConnectionException() << PositionInfo(position);

    if(iter->first == previous)
        iter->first = current;
    else if(iter->second == previous)
        iter->second = current;
    else
        throw UnknownConnectionException() << PositionInfo(position);  
};