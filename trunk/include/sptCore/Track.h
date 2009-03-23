#ifndef SPTCORE_TRACK_H
#define SPTCORE_TRACK_H 1

#include "sptCore/RailTracking.h"
#include "sptCore/Path.h"

namespace sptCore
{

class Track: public RailTracking
{

public:
    Track(osg::Vec3 p1, osg::Vec3 p2);
    Track(osg::Vec3 p1, osg::Vec3 cp1, osg::Vec3 p2, osg::Vec3 cp2);

    virtual ~Track() { };

    virtual osg::Vec3 getExit(osg::Vec3 entry) const;
    virtual Path* getPath(osg::Vec3 entry) const;
    virtual Path* reverse(Path* path) const;

private:
    Path::Pair _path;

};

} // namespace sptCore

#endif // headerguard
