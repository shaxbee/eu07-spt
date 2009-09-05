#ifndef SPTCORE_TRACK_H
#define SPTCORE_TRACK_H 1

#include <sptCore/RailTracking.h>

namespace sptCore
{

class Track: public RailTracking
{

public:
    //! Construct straight track
    Track(osg::Vec3 p1, osg::Vec3 p2);

    //! Construct bezier track
    Track(osg::Vec3 p1, osg::Vec3 cp1, osg::Vec3 p2, osg::Vec3 cp2);

    virtual ~Track() { };

    virtual osg::Vec3 getExit(const osg::Vec3& entry) const;
    virtual Path* getPath(const osg::Vec3& entry) const;

    virtual Path* getDefaultPath() const { return NULL; };

//    virtual void enter(Follower* follower, const osg::Vec3& entry) { };
//    virtual void leave(Follower* follower, const osg::Vec3& entry) { };

private:
    Path* _forward;
    Path* _backward;

};

} // namespace sptCore

#endif // headerguard
