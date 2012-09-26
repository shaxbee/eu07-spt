#include "sptCore/Track.h"

namespace sptCore
{

Track::Track(TrackId id, const osg::Vec2f& sector):
    _id(id),
	_sector(sector)
{
}

const TrackId& Track::getId() const
{
    return _id;
}    

const osg::Vec2f& Track::getSector() const
{
    return _sector;
}    

Track::~Track()
{
};

}; // namespace sptCore
