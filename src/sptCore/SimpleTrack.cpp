#include "sptCore/SimpleTrack.h"

using namespace sptCore;

osg::Vec3 SimpleTrack::getExit(const osg::Vec3& entry) const
{

    // if entrance == track begin
    if(entry == _path->front())
        return _path->back();

    // if entrance == track end
    if(entry == _path->back())
        return _path->front();

    throw UnknownEntryException() << PositionInfo(entry);

}; // Track::getNext

std::auto_ptr<Path> SimpleTrack::getPath(const osg::Vec3& entry) const
{
    if(entry == _path->front())
        return _path->clone();

    if(entry == _path->back())
        return _path->reverse();

    throw UnknownEntryException() << PositionInfo(entry);
}; // Track::getPath
