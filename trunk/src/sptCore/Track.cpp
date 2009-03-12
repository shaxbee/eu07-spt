#include "sptCore/Track.h"

using namespace sptCore;

Track::Track(osg::Vec3 p1, osg::Vec3 p2):
    _path(Path::straight(p1, p2))
{

}; // Track::Track(p1, p2)

Track::Track(osg::Vec3 p1, osg::Vec3 p2, osg::Vec3 cp1, osg::Vec3 cp2):
    _path(Path::bezier(p1, p2, cp1, cp2))
{

}; // Track::Track(p1, p2, cp1, cp2)

osg::Vec3 Track::getExit(osg::Vec3 entry)
{

    // if entrance == track begin
    if(entry == _path.first->front())
        return _path.first->back();

    // if entrance == track end
    if(entry == _path.second->front())
        return _path.second->back();

    throw UnknownEntryException() << PositionInfo(entry);

}; // RailTracking::getNext

Path* Track::getPath(osg::Vec3 entry)
{

    if(entry == _path.first->front())
        return _path.first.get();

    if(entry == _path.second->front())
        return _path.second.get();

    throw UnknownEntryException() << PositionInfo(entry);

}; // RailTracking::getPath
