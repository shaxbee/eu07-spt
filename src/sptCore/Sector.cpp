#include "sptCore/Sector.h"

#include <boost/functional/hash.hpp>

using namespace sptCore;

float Sector::SIZE = 2000.0;

namespace osg
{
size_t hash_value(const osg::Vec3f& value)
{
	size_t result = 0;
	boost::hash_combine(result, value.x());
	boost::hash_combine(result, value.y());
	boost::hash_combine(result, value.z());
}
};

Sector::Sector(const osg::Vec3f& position, Tracks& trackings, Externals& connections): _position(position)
{
    _trackings.swap(trackings);
    _externals.swap(connections);
}; // Sector::Sector(scenery)

const Track& Sector::getTrack(const TrackId id) const
{
    return _trackings.at(id.value());
};
