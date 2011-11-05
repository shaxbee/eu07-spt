#ifndef SPTCORE_RAILTRACKING_H
#define SPTCORE_RAILTRACKING_H 1

#include <osg/Vec3>
#include <osg/Matrix>

#include <boost/exception/all.hpp>

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
    RailTracking(Sector& sector);
    virtual ~RailTracking();

    //! Get tracking exit for given entry point
    //! \throw UnknownEntryException if there is no exit for given entry
    virtual osg::Vec3 getExit(const osg::Vec3& entry) const = 0;

    //! Get path that begins at given position
    //! \throw UnknownEntryException if there is no path for given entry
    virtual std::auto_ptr<Path> getPath(const osg::Vec3& entry) const = 0;

    Sector& getSector() const { return _sector; }

    typedef boost::error_info<struct tag_position, osg::Vec3f> PositionInfo;
    class UnknownEntryException: public boost::exception { };

    bool operator<(const RailTracking& other) const { return this < &other; }

private:
    Sector& _sector;

}; // class sptCore::RailTracking

} // namespace sptCore

#endif // headerguard
