#include "sptCore/Sector.h"
#include "sptCore/TrackVisitor.h"

#include <boost/functional/hash.hpp>
#include <boost/bind.hpp>

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

	return result;
}
};

Sector::Sector(const osg::Vec3f& position, Tracks& trackings): _position(position)
{
    _trackings.swap(trackings);
}; // Sector::Sector(scenery)

const Track& Sector::getTrack(const TrackId id) const
{
    return _trackings.at(id.value());
};

void Sector::accept(TrackVisitor& visitor) const
{
    std::for_each(_trackings.begin(), _trackings.end(), boost::bind(&Track::accept, _1, boost::ref(visitor)));
};
