#ifndef SPTCORE_TRACK_H
#define SPTCORE_TRACK_H 1

#include "Path.h"
#include "TrackLocator.h"

#include <stdint.h>

#include <osg/Vec3>
#include <osg/Matrix>

#include <boost/exception/all.hpp>

namespace sptCore
{

class TrackVisitor;

//! \brief Abstract representation of railway tracking
//! \author Zbyszek "ShaXbee" Mandziejewicz
class Track
{

public:
	Track(const osg::Vec2f& sector);
    virtual ~Track();

    const osg::Vec2f& getSector() const;

    virtual void accept(TrackVisitor& visitor) const = 0;

    //! Get tracking exit for given entry point
    //! \throw UnknownEntryException if there is no exit for given entry
    virtual osg::Vec3 getExit(const osg::Vec3& entry) const = 0;

    //! Get path that begins at given position
    //! \throw UnknownEntryException if there is no path for given entry
    virtual std::shared_ptr<const Path> getPath(const osg::Vec3& entry) const = 0;

    //! Get connected track
    virtual TrackId getNextTrack(const osg::Vec3& entry) const = 0;

    typedef boost::error_info<struct tag_position, osg::Vec3f> PositionInfo;
    class UnknownEntryException: public boost::exception { };

private:
    osg::Vec2f _sector;

}; // class sptCore::Track

}; // namespace sptCore

#endif // headerguard
