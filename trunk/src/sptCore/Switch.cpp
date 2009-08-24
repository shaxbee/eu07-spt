#include "sptCore/Switch.h"

using namespace sptCore;

Switch::Switch(osg::Vec3 p1, osg::Vec3 cp1, osg::Vec3 p2, osg::Vec3 cp2, osg::Vec3 p3, osg::Vec3 cp3, Switch::Position position):
    _straight(Path::bezier(p1, cp1, p2, cp2, 32)),
    _diverted(Path::bezier(p1, cp1, p3, cp3, 32)),
    _position(position)
{

}; // Switch::Switch(p1, cp1, p2, cp2, p3, cp3)

osg::Vec3 Switch::getExit(const osg::Vec3& entry) const
{
    
    // entry == begin
    if(entry == _straight.first->front())
        if(_position == STRAIGHT)
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
        if(_position == STRAIGHT)
            return _straight.first;
        else
            return _diverted.first;

    if(entry == _straight.second->front())
       return _straight.second;

    if(entry == _diverted.first->front())
       return _diverted.first;

    if(entry == _diverted.second->front())
       return _diverted.second;

    throw UnknownEntryException() << PositionInfo(entry);

}; // Switch::getPath(entry)
