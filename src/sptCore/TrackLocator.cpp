#include "sptCore/TrackLocator.h"

#include <limits>

namespace sptCore
{

TrackId::TrackId(uint32_t value):
    _value(value)
{
}

bool TrackId::operator==(const TrackId& other) const
{
    return _value == other._value;
}

TrackId::operator bool() const
{
    return _value != null()._value;
}

bool TrackId::isExternal() const
{
    return _value == external()._value;
}

TrackId TrackId::null()
{
    return TrackId(std::numeric_limits<uint32_t>::max());
}

TrackId TrackId::external() 
{
    return TrackId(std::numeric_limits<uint32_t>::max() - 1);
}

TrackLocator::TrackLocator(const osg::Vec2f& sector, TrackId id):
    _sector(sector), _id(id)
{
}

bool TrackLocator::operator==(const TrackLocator& other) const
{
    return (_sector == other._sector) && (_id == other._id);
}
    
TrackLocator::operator bool() const
{
    return bool(_id);
}    

static TrackLocator null()
{
    return { osg::Vec2f(), TrackId::null() };
} 

}; // namespace sptCore
