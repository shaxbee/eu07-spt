#include "sptCore/Switch.h"
#include "sptCore/TrackVisitor.h"

#include <boost/assign/list_of.hpp>

using namespace sptCore;
using namespace boost::assign;

void Switch::accept(TrackVisitor& visitor) const
{
    visitor.apply(*this);
}; // Switch::accept

osg::Vec3 Switch::getExit(const osg::Vec3& entry) const
{
    
    // entry == begin
    if(entry == _straight->front())
        return (getPosition() == "STRAIGHT") ? _straight->back() : _diverted->back();

    if(entry == _straight->back())
        return _straight->front();

    if(entry == _diverted->front())
        return _diverted->back();

    if(entry == _diverted->back())
        return _diverted->front();

    throw UnknownEntryException() << PositionInfo(entry);
}; // Switch::getExit(entry)

std::shared_ptr<const Path> Switch::getPath(const osg::Vec3& entry) const
{
    if(entry == _straight->front())
    {
        if(getPosition() == "STRAIGHT")
        {
            return _straight->clone();
        }
        else
        {
            return _diverted->clone();
        };
    };

    if(entry == _straight->back())
    {
        return _straight->reverse();
    };

    if(entry == _diverted->back())
    {
       return _diverted->reverse();
    }

    throw std::invalid_argument("Unknown entry");
}; // Switch::getPath(entry)

TrackId Switch::getNextTrack(const osg::Vec3& entry) const
{
    if(entry == _straight->front())
    {
        return _commonId; 
    };

    if(entry == _straight->back())
    {
        return _straightId;
    };

    if(entry == _diverted->back())
    {
        return _divertedId;
    };
    
    throw UnknownEntryException() << PositionInfo(entry);
};

std::vector<std::string> Switch::getValidPositions() const
{
    return {"STRAIGHT", "DIVERTED"};
}; // Switch::getValidPositions
