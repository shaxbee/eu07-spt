#ifndef SPTCORE_TRACK_H
#define SPTCORE_TRACK_H 1

#include <osg/Vec3>
#include <osg/Matrix>

#include <boost/exception/all.hpp>

#include <sptCore/Path.h>

namespace sptCore
{

class TrackId
{
public:
    explicit TrackId(uint32_t value);

    bool isNull() const;
    bool isExternal() const;

    uint32_t value() const;

private:
    uint32_t _value;
};

//! \brief Abstract representation of railway tracking
//! \author Zbyszek "ShaXbee" Mandziejewicz
class Track
{

public:
	Track(const osg::Vec3f& sector);
    virtual ~Track();

    osg::Vec3f getSector() const;

    //! Get tracking exit for given entry point
    //! \throw UnknownEntryException if there is no exit for given entry
    virtual osg::Vec3 getExit(const osg::Vec3& entry) const = 0;

    //! Get path that begins at given position
    //! \throw UnknownEntryException if there is no path for given entry
    virtual std::auto_ptr<Path> getPath(const osg::Vec3& entry) const = 0;

    //! Get connected track
    virtual TrackId getNextTrack(const osg::Vec3& entry) const = 0;

    typedef boost::error_info<struct tag_position, osg::Vec3f> PositionInfo;
    class UnknownEntryException: public boost::exception { };

private:
    osg::Vec3f _sector;

}; // class sptCore::Track

}; // namespace sptCore

#endif // headerguard
