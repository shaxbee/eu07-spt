#include "sptCore/Switch.h"

using namespace sptCore;

SwitchableTracking::ValidPositions Switch::_positions;

Switch::Switch(Sector& sector,  std::auto_ptr<Path> straight, std::auto_ptr<Path> diverted, const std::string& position):
    SwitchableTracking(sector), 
    _straight(straight.release()), 
    _diverted(diverted.release())
{

    setPosition(position);

}; // Switch::Switch(p1, cp1, p2, cp2, p3, cp3, position)

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
       return getStraightReversed();

    if(entry == _diverted->front())
       return *_diverted;

    if(entry == _diverted->back())
       return getDivertedReversed(); 

    throw UnknownEntryException() << PositionInfo(entry);

}; // Switch::getPath(entry)


const SwitchableTracking::ValidPositions Switch::getValidPositions() const
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
