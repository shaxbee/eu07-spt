#include "sptCore/Track.h"

using namespace sptCore;

Track::Track(osg::Vec3 p1, osg::Vec3 p2):
    _path(Path::straight(p1, p2))
{

}; // Track::Track(p1, p2)

Track::Track(osg::Vec3 p1, osg::Vec3 cp1, osg::Vec3 p2, osg::Vec3 cp2):
    _path(Path::bezier(p1, cp1, p2, cp2, 32))
{

}; // Track::Track(p1, p2, cp1, cp2)

osg::Vec3 Track::getExit(osg::Vec3 entry) const
{

    // if entrance == track begin
    if(entry == _path.first->front())
        return _path.first->back();

    // if entrance == track end
    if(entry == _path.second->front())
        return _path.second->back();

    throw UnknownEntryException() << PositionInfo(entry);

}; // RailTracking::getNext

Path* Track::getPath(osg::Vec3 entry) const
{

    if(entry == _path.first->front())
        return _path.first.get();

    if(entry == _path.second->front())
        return _path.second.get();

    throw UnknownEntryException() << PositionInfo(entry);

}; // RailTracking::getPath

Path* Track::reverse(Path* path) const
{
    
    if(path == _path.first)
        return _path.second.get();
    
    if(path == _path.second)
        return _path.first.get();
    
    throw UnknownPathException() << PathInfo(path);
    
}; // RailTracking::reverse
