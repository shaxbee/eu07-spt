#ifndef SPTCORE_TRACK_H
#define SPTCORE_TRACK_H 1

#include <sptCore/RailTracking.h>

#include <boost/scoped_ptr.hpp>

namespace sptCore
{

class Track: public RailTracking
{

public:
    //! Construct straight track
    Track(Sector& sector, osg::Vec3 p1, osg::Vec3 p2);

    //! Construct bezier track
    Track(Sector& sector, osg::Vec3 p1, osg::Vec3 cp1, osg::Vec3 p2, osg::Vec3 cp2);

    virtual ~Track() { };

    virtual const osg::Vec3& getExit(const osg::Vec3& entry) const;
    virtual const Path& getPath(const osg::Vec3& entry) const;

    //! \brief Get default (forward) path
    const Path& getDefaultPath() const { return *_forward; }
    
private:
    boost::scoped_ptr<Path> _forward;
    boost::scoped_ptr<Path> _backward;

};

} // namespace sptCore

#endif // headerguard
