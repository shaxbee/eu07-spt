#include "sptCore/Switch.h"

using namespace sptCore;

Switch::_positions = ValidPositions();

Switch::_positions.reserve(2);
Switch::_positions.push_back("STRAIGHT");
Switch::_positions.push_back("DIVERTED");

Switch::Switch(const osg::Vec3& p1, const osg::Vec3& cp1, const osg::Vec3& p2, const osg::Vec3& cp2, const osg::Vec3& p3, const osg::Vec3& cp3, const std::string& position)
{
    _straight.first = new Path(p1, cp1, p2, cp2, 32);
    _straight.second = _straight.first->reverse();
    _diverted.first = new Path(p1, cp1, p3, cp3, 32);
    _diverted.second = _diverted.first->reverse();
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
