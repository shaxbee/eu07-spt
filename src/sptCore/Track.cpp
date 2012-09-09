#include "sptCore/Track.h"

#include <limits>

using namespace sptCore;

TrackId::TrackId(uint32_t value):
    _value(value)
{
}

bool TrackId::operator==(TrackId other) const
{
    return _value == other._value;
}

bool TrackId::isNull() const
{
    return *this == null();
}

bool TrackId::isExternal() const
{
    return *this == external();
}

uint32_t TrackId::value() const
{
    return _value;
}

TrackId TrackId::null()
{
    return TrackId(std::numeric_limits<uint32_t>::max());
}

TrackId TrackId::external() 
{
    return TrackId(std::numeric_limits<uint32_t>::max() - 1);
}

Track::Track(const osg::Vec2f& sector):
	_sector(sector)
{

}

const osg::Vec2f& Track::getSector() const
{
    return _sector;
}    

Track::~Track()
{
};
