#ifndef SPTCORE_TRACK_H
#define SPTCORE_TRACK_H 1

#include <osg/Vec3>
#include <boost/scoped_ptr.hpp>

#include "sptCore/RailTracking.h"

namespace sptCore
{

class Track: public RailTracking
{

public:
    Track(osg::Vec3 p1, osg::Vec3 p2, RailTracking* previous);
    Track(osg::Vec3 p1, osg::Vec3 p2, osg::Vec3 cp1, osg::Vec3 cp2, RailTracking* previous);

    virtual ~Track();

    virtual RailTracking* getNext(RailTracking* tracking);
    virtual Path* getPath(RailTracking* tracking);
    virtual Path* reverse(Path* path);

    inline void setPrevious(RailTracking* previous) { _path->_previous = previous; };
    inline void setNext(RailTracking* next) { _path->_next = next; };

private:
    boost::scoped_ptr<Path> _path;
    boost::scoped_ptr<Path> _reversedPath;

    boost::scoped_ptr<RailTracking> _previous;
    boost::scoped_ptr<RailTracking> _next;

};

} // namespace sptCore

#endif // headerguard
