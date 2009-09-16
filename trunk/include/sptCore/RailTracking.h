#ifndef SPTCORE_RAILTRACKING_H
#define SPTCORE_RAILTRACKING_H 1

#include <osg/Vec3>
#include <osg/Matrix>

#include <boost/exception.hpp> 

#include <sptCore/Path.h>

namespace sptCore
{

class Sector;
class Follower;

//! \brief Abstract representation of railway tracking
//! \author Zbyszek "ShaXbee" Mandziejewicz
class RailTracking
{

public:
    RailTracking(Sector& sector): _sector(sector) { };
    virtual ~RailTracking() { };

    //! Get tracking exit for given entry point
    //! \throw UnknownEntryException if there is no exit for given entry
    virtual const osg::Vec3& getExit(const osg::Vec3& entry) const = 0;

    //! Get path that begins at given position
    //! \throw UnknownEntryException if there is no path for given entry
    virtual const Path& getPath(const osg::Vec3& entry) const = 0;

    Sector& getSector() const { return _sector; }

    //! Check if there are any followers on tracking
    bool isOccupied() const { return _followersCount != 0; }

    size_t getFollowersCount() const { return _followersCount; }

    //! Register follower entering tracking
    virtual void enter(Follower& follower, const osg::Vec3& entry) { _followersCount++; }
    
    //! Register follower leaving tracking
    virtual void leave(Follower& follower, const osg::Vec3& entry) { _followersCount--; }

    typedef boost::error_info<struct tag_position, osg::Vec3f> PositionInfo;
    class UnknownEntryException: public boost::exception { };
    
private:
    Sector& _sector;
    size_t _followersCount;

}; // class sptCore::RailTracking

} // namespace sptCore

#endif // headerguard
