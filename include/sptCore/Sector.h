#ifndef SPTCORE_SECTOR_H
#define SPTCORE_SECTOR_H 1

#include <vector>

#include <boost/tr1/unordered_map.hpp>
#include <boost/ptr_container/ptr_vector.hpp>

#include <osg/Vec3f>

#include "sptCore/Track.h"

namespace sptCore
{

typedef boost::ptr_vector<Track> Tracks;

struct External
{
    const TrackId track;
    const osg::Vec3f sector;
};

typedef std::tr1::unordered_map<osg::Vec3f, External> Externals;

class TrackVisitor;

//! Container for rail trackings located in chunk of Scenery
//! \author Zbigniew "ShaXbee" Mandziejewicz
class Sector
{
public:
    Sector(const osg::Vec3f& position, Tracks& trackings);

    const osg::Vec3f& getPosition() const { return _position; };

    const External getExternal(const osg::Vec3f& position);
    const Track& getTrack(const TrackId index) const;

    void accept(TrackVisitor& visitor) const;

    typedef boost::error_info<struct tag_position, osg::Vec3f> PositionInfo;
    class UnknownConnectionException: public boost::exception { };

    static float SIZE;

private:
    const osg::Vec3f _position;
    Externals _externals;
    Tracks _trackings;
}; // class sptCore::Sector

} // namespace sptCore

#endif // header guard
