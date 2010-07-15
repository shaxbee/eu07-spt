#include "sptCore/Switch.h"

using namespace sptCore;

SwitchableTracking::ValidPositions Switch::_positions;

Switch::~Switch()
{

}; // Switch::~Switch

const osg::Vec3& Switch::getExit(const osg::Vec3& entry) const
{
    
    // entry == begin
    if(entry == _straight->front())
        if(getPosition() == "STRAIGHT")
            return _straight->back();
        else
            return _diverted->back();

    if(entry == _straight->back())
        return _straight->front();

    if(entry == _diverted->front())
        return _diverted->back();

    if(entry == _diverted->back())
        return _diverted->front();

    throw UnknownEntryException() << PositionInfo(entry);

}; // Switch::getExit(entry)

const Path& Switch::getPath(const osg::Vec3& entry) const
{

    if(entry == _straight->front())
        if(getPosition() == "STRAIGHT")
            return *_straight;
        else
            return *_diverted;

    if(entry == _straight->back())
       return *_straightReversed;

    if(entry == _diverted->front())
       return *_diverted;

    if(entry == _diverted->back())
       return *_divertedReversed; 

    throw UnknownEntryException() << PositionInfo(entry);

}; // Switch::getPath(entry)

const Path& Switch::reversePath(const Path& path) const
{
    if(&path == _straight.get())
        return *_straightReversed;

    if(&path == _straightReversed.get())
        return *_straight;

    if(&path == _diverted.get())
        return *_divertedReversed;

    if(&path == _divertedReversed.get())
        return *_diverted;

    throw std::logic_error("Unknown path");
}; // Switch::reversePath

const SwitchableTracking::ValidPositions& Switch::getValidPositions() const
{

    static bool initialized = false;

    if(!initialized)
    {
        _positions.push_back("STRAIGHT");
        _positions.push_back("DIVERTED");
        initialized = true;
    };

    return _positions;

}; // Switch::getValidPositions
