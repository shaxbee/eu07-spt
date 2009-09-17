#include "sptCore/Switch.h"

using namespace sptCore;

SwitchableTracking::ValidPositions Switch::_positions;

Switch::Switch(Sector& sector, const osg::Vec3& p1, const osg::Vec3& cp1, const osg::Vec3& p2, const osg::Vec3& cp2, const osg::Vec3& p3, const osg::Vec3& cp3, const std::string& position):
    SwitchableTracking(sector)
{

    Path* path = new Path(p1, cp1, p2, cp2, 32);
    _straight = std::make_pair(path, path->reverse());

    path = new Path(p1, cp1, p3, cp3, 32);
    _diverted = std::make_pair(path, path->reverse());

    setPosition(position);

}; // Switch::Switch(p1, cp1, p2, cp2, p3, cp3, position)

Switch::~Switch()
{

    delete _straight.first;
    delete _straight.second;
    delete _diverted.first;
    delete _diverted.second;

}; // Switch::~Switch

const osg::Vec3& Switch::getExit(const osg::Vec3& entry) const
{
    
    // entry == begin
    if(entry == _straight.first->front())
        if(_position == "STRAIGHT")
            return _straight.first->back();
        else
            return _diverted.first->back();

    if(entry == _straight.second->front())
        return _straight.second->back();

    if(entry == _diverted.first->front())
        return _diverted.first->back();

    if(entry == _diverted.second->front())
        return _diverted.second->back();

    throw UnknownEntryException() << PositionInfo(entry);

}; // Switch::getExit(entry)

const Path& Switch::getPath(const osg::Vec3& entry) const
{

    if(entry == _straight.first->front())
        if(_position == "STRAIGHT")
            return *_straight.first;
        else
            return *_diverted.first;

    if(entry == _straight.second->front())
       return *_straight.second;

    if(entry == _diverted.first->front())
       return *_diverted.first;

    if(entry == _diverted.second->front())
       return *_diverted.second;

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
