#include "sptCore/Sector.h"

using namespace sptCore;

float Sector::SIZE = 2000.0;

const RailTracking& Sector::getNextTrack(const osg::Vec3& position, const RailTracking& from) const
{
    Connection search = {position, NULL, NULL};

    Connections::const_iterator iter = std::lower_bound(_connections.begin(), _connections.end(), search, ConnectionLess());

    assert(iter->position == position);
    assert(iter->first == from || iter->second == from);

    return iter->first == from ? second : first;
}; // Sector::getNextTrack(position, from)

size_t Sector::getTracksCount() const
{
    return _connections.size();
}; // Sector::getTracksCount()
