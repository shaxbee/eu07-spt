#include "sptCore/Track.h"

using namespace sptCore;

Track::Track(osg::Vec3 p1, osg::Vec3 p2):
    _forward(new Path(p1, p2))
{
    _backward = _forward->reverse();
}; // Track::Track(p1, p2)

Track::Track(osg::Vec3 p1, osg::Vec3 cp1, osg::Vec3 p2, osg::Vec3 cp2):
    _forward(new Path(p1, cp1, p2, cp2, 32))
{
    _backward = _forward->reverse();
}; // Track::Track(p1, p2, cp1, cp2)

osg::Vec3 Track::getExit(const osg::Vec3& entry) const
{

    // if entrance == track begin
    if(entry == _forward->front())
        return _forward->back();

    // if entrance == track end
    if(entry == _forward->back())
        return _forward->front();

    throw UnknownEntryException() << PositionInfo(entry);

}; // RailTracking::getNext

Path* Track::getPath(const osg::Vec3& entry) const
{

    if(entry == _forward->front())
        return _forward;

    if(entry == _backward->front())
        return _backward;

    throw UnknownEntryException() << PositionInfo(entry);

}; // RailTracking::getPath
