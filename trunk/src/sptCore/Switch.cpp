#include "sptCore/Switch.h"

using namespace sptCore;

Switch::Switch(osg::Vec3 p1, osg::Vec3 cp1, osg::Vec3 p2, osg::Vec3 cp2, osg::Vec3 p3, osg::Vec3 cp3):
    _straight(Path::bezier(p1, cp1, p2, cp2)),
    _diverted(Path::bezier(p1, cp1, p3, cp3)),
    _position(STRAIGHT)
{

}; // Switch::Switch(p1, cp1, p2, cp2, p3, cp3)

osg::Vec3 Switch::getExit(osg::Vec3 entry)
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

Path* Switch::getPath(osg::Vec3 entry)
{

    if(entry == _straight.first->front())
        if(_position == STRAIGHT)
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

