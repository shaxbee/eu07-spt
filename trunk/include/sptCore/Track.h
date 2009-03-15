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
    Track(osg::Vec3 p1, osg::Vec3 p2);
    Track(osg::Vec3 p1, osg::Vec3 cp1, osg::Vec3 p2, osg::Vec3 cp2);

    virtual ~Track();

    virtual osg::Vec3 getExit(osg::Vec3 entry);
    virtual Path* getPath(osg::Vec3 entry);
    virtual Path* reverse(Path* path);

private:
    Path::Pair _path;

};

} // namespace sptCore

#endif // headerguard
