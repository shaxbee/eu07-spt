#include "sptCore/Track.h"

using namespace sptCore;

const osg::Vec3& Track::getExit(const osg::Vec3& entry) const
{

    // if entrance == track begin
    if(entry == _forward->front())
        return _forward->back();

    // if entrance == track end
    if(entry == _forward->back())
        return _forward->front();

    throw UnknownEntryException() << PositionInfo(entry);

}; // Track::getNext

const Path& Track::getPath(const osg::Vec3& entry) const
{

    if(entry == _forward->front())
        return *_forward;

    if(entry == _forward->back())
        return *_backward;

    throw UnknownEntryException() << PositionInfo(entry);

}; // Track::getPath
