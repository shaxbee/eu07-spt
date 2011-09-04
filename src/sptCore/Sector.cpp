#include "sptCore/Sector.h"

using namespace sptCore;

float Sector::SIZE = 2000.0;

Sector::Sector(const osg::Vec3d& position, RailTrackings& trackings, Connections& connections): _position(position)
{
    _trackings.swap(trackings);
    _connections.swap(connections);
}; // Sector::Sector(scenery)

const RailTracking& Sector::getNextRailTracking(const osg::Vec3f& position, const size_t from) const
{
    Connections::const_iterator iter = _connections.find(position);

    if(iter == _connections.end() || (iter->first != from && iter->second != from))
    {
        throw UnknownConnectionException() << PositionInfo(position);
    };

    return (iter->first == from) ? iter->second : iter->first;
}; // Sector::getNextTrack(position, from)

const RailTracking& Sector::getRailTracking(const size_t index) const
{
    return _trackings.at(index);
};

size_t Sector::getRailTrackingCount() const
{
    return _trackings.size();
}; // Sector::getRailTrackingCount()