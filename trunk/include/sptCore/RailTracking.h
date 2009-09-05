#ifndef SPTCORE_RAILTRACKING_H
#define SPTCORE_RAILTRACKING_H 1

#include <osg/Vec3>
#include <boost/exception.hpp> 

#include <sptCore/Path.h>

namespace sptCore
{

// class Follower;

//! \brief Abstract representation of Tracking in Scenery
//! \author Zbyszek "ShaXbee" Mandziejewicz
class RailTracking
{

public:
    virtual ~RailTracking() { };

    //! Get tracking exit for given entry point
    //! Throws UnknownEntryException if there is no exit for given entry
    virtual osg::Vec3 getExit(const osg::Vec3& entry) const = 0;

    //! Get path that begins at given position
    //! Throws UnknownEntryException if there is no path for given entry
    virtual Path* getPath(const osg::Vec3& entry) const = 0;

//    virtual void enter(Follower* follower, const osg::Vec3& entry) = 0;
//    virtual void leave(Follower* follower, const osg::Vec3& entry) = 0;

    typedef boost::error_info<struct tag_position, osg::Vec3f> PositionInfo;
    class UnknownEntryException: public boost::exception { };

}; // class sptCore::RailTracking

} // namespace sptCore

#endif // headerguard
