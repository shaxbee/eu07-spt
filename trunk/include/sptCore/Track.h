#ifndef SPTCORE_TRACK_H
#define SPTCORE_TRACK_H 1

#include <sptCore/RailTracking.h>

#include <boost/shared_ptr.hpp>

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

    //! \brief Get default (forward) path
    virtual Path* getPath() const { return _forward.get(); }
    
private:
    boost::shared_ptr<Path> _forward;
    boost::shared_ptr<Path> _backward;

};

} // namespace sptCore

#endif // headerguard
