#include "sptCore/SimpleTrack.h"
#include "sptCore/TrackVisitor.h"

#include <stdexcept>
#include <boost/format.hpp>

using boost::format;
using boost::str;

namespace sptCore
{

SimpleTrack::SimpleTrack(const osg::Vec2f& sector, std::shared_ptr<Path> path, TrackId front, TrackId back):
    Track(sector),
    _path(path),
    _front(front),
    _back(back)
{
}; // SimpleTrack::SimpleTrack

SimpleTrack::SimpleTrack(SimpleTrack&& other):
    Track(other.getSector()),
    _path(std::move(other._path)),
    _front(other._front),
    _back(other._back)    
{
};

SimpleTrack::~SimpleTrack()
{
}; // SimpleTrack::~SimpleTrack

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

std::shared_ptr<const Path> SimpleTrack::getPath(const osg::Vec3& entry) const
{
    if(entry == _path->front())
    {    
        return _path;
    }    

    if(entry == _path->back())
    {    
        return _path->reverse();
    }    

    throw UnknownEntryException() << PositionInfo(entry);
}; // SimpleTrack::getPath

std::shared_ptr<const Path> SimpleTrack::getDefaultPath() const
{
    return _path;
}; // SimpleTrack::getDefaultPath    

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

    throw std::invalid_argument(str(format("Unknown entry (%s, %s, %s)") % entry.x() % entry.y() % entry.z()));
}; // SimpleTrack::getNextTrack

}; // namespace sptCore
