#include "sptCore/Track.h"

using namespace sptCore;

Track::Track(osg::Vec3 p1, osg::Vec3 p2, RailTracking* previous)
{
//    _path = Path::straight(p1, p2, previous, NULL);

}; // Track::Track(p1, p2, previous)

Track::Track(osg::Vec3 p1, osg::Vec3 p2, osg::Vec3 cp1, osg::Vec3 cp2, RailTracking* previous):
    _path(Path::bezier(p1, p2, cp1, cp2, previous, NULL))
{

}; // Track::Track(p1, p2, cp1, cp2, previous)

RailTracking* Track::getNext(RailTracking* tracking)
{

    if(tracking == _path->_previous)
        return _path->_next;

    if(tracking == _path->_next)
        return _path->_previous;

//    throw RailTrackingException("Unknown tracking");

}; // RailTracking::getNext

Path* Track::getPath(RailTracking* tracking)
{

    if(tracking == _path->_previous)

        return _path.get();

    if(tracking == _path->_next)
    {

        if(!_reversedPath)
            _reversedPath.reset(_path->reverse());

        return _reversedPath.get();

    };

//    throw RailTrackingException("Unknown tracking");

}; // RailTracking::getPath
