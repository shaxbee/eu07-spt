#include "sptCore/Switch.h"

using namespace sptCore;

SwitchableTracking::ValidPositions Switch::_positions;

Switch::Switch(const osg::Vec3& p1, const osg::Vec3& cp1, const osg::Vec3& p2, const osg::Vec3& cp2, const osg::Vec3& p3, const osg::Vec3& cp3, const std::string& position)
{
    _straight.first.reset(new Path(p1, cp1, p2, cp2, 32));
    _straight.second.reset(_straight.first->reverse());
    _diverted.first.reset(new Path(p1, cp1, p3, cp3, 32));
    _diverted.second.reset(_diverted.first->reverse());
    setPosition(position);
}; // Switch::Switch(p1, cp1, p2, cp2, p3, cp3, position)

osg::Vec3 Switch::getExit(const osg::Vec3& entry) const
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

Path* Switch::getPath(const osg::Vec3& entry) const
{

    if(entry == _straight.first->front())
        if(_position == "STRAIGHT")
            return _straight.first.get();
        else
            return _diverted.first.get();

    if(entry == _straight.second->front())
       return _straight.second.get();

    if(entry == _diverted.first->front())
       return _diverted.first.get();

    if(entry == _diverted.second->front())
       return _diverted.second.get();

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
