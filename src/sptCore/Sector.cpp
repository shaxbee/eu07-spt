#include "sptCore/Sector.h"

using namespace sptCore;

float Sector::SIZE = 2000.0;

Sector::Sector(Scenery& scenery, const osg::Vec3d& position): _scenery(scenery), _position(position)
{

}; // Sector::Sector(scenery)

const RailTracking& Sector::getNextTrack(const osg::Vec3& position, const RailTracking& from) const
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

size_t Sector::getTracksCount() const
{
    return _connections.size();
}; // Sector::getTracksCount()