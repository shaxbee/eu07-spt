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

Sector::Sector(const osg::Vec2f& position, Tracks&& tracks): 
    _position(position),
    _tracks(std::move(tracks))
{
}; // Sector::Sector(scenery)

const Track& Sector::getTrack(const TrackId id) const
{
    const auto& track = _tracks.at(id.value());

    if(!track)
    {
        throw std::logic_error("Invalid track");
    };
        
    return *track;
};

void Sector::accept(TrackVisitor& visitor) const
{
    for(auto& track: _tracks)
    {
        track->accept(visitor);
    };    
};
