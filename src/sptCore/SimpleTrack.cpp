#include "sptCore/SimpleTrack.h"
#include "sptCore/TrackVisitor.h"

using namespace sptCore;

void SimpleTrack::accept(TrackVisitor& visitor) const
{
    visitor.apply(*this);
}; // SimpleTrack::accept

osg::Vec3 SimpleTrack::getExit(const osg::Vec3& entry) const
{

    // if entrance == track begin
    if(entry == _path->front())
        return _path->back();

    // if entrance == track end
    if(entry == _path->back())
        return _path->front();

    throw UnknownEntryException() << PositionInfo(entry);

}; // SimpleTrack::getNext

std::auto_ptr<Path> SimpleTrack::getPath(const osg::Vec3& entry) const
{
    if(entry == _path->front())
        return _path->clone();

    if(entry == _path->back())
        return _path->reverse();

    throw UnknownEntryException() << PositionInfo(entry);
}; // SimpleTrack::getPath

TrackId SimpleTrack::getNextTrack(const osg::Vec3& entry) const
{
    if(entry == _path->front())
    {
        return _front;
    };

    if(entry == _path->back())
    {
        return _back;
    };

    throw UnknownEntryException() << PositionInfo(entry);
}; // SimpleTrack::getNextTrack

