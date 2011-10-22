#include "sptCore/Switch.h"

#include <boost/assign/list_of.hpp>

using namespace sptCore;
using namespace boost::assign;

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

std::auto_ptr<Path> Switch::getPath(const osg::Vec3& entry) const
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

    throw UnknownEntryException() << PositionInfo(entry);
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

const SwitchableTracking::ValidPositions& Switch::getValidPositions() const
{
    static ValidPositions positions = list_of("STRAIGHT")("DIVERTED");
    return positions;
}; // Switch::getValidPositions
