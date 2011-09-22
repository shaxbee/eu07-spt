#ifndef SPTCORE_SECTOR_H
#define SPTCORE_SECTOR_H 1

#include <vector>

#include <boost/cstdint.hpp>
#include <boost/tr1/unordered_map.hpp>
#include <boost/ptr_container/ptr_vector.hpp>

#include <osg/Vec3f>

#include "sptCore/Track.h"

namespace sptCore
{

typedef boost::ptr_vector<Track> RailTrackings;

struct External
{
    const TrackId track;
    const osg::Vec3f sector;
};

typedef std::tr1::unordered_map<osg::Vec3f, External> Externals;

//! Container for rail trackings located in chunk of Scenery
//! \author Zbigniew "ShaXbee" Mandziejewicz
class Sector
{
public:
    Sector(const osg::Vec3f& position, RailTrackings& trackings, Externals& externals);

    const osg::Vec3f& getPosition() const { return _position; };

    const External getExternal(const osg::Vec3f& position);
    const Track& getTrack(const TrackId index) const;

    typedef boost::error_info<struct tag_position, osg::Vec3f> PositionInfo;
    class UnknownConnectionException: public boost::exception { };

    static float SIZE;

private:
    const osg::Vec3f _position;
    Externals _externals;
    RailTrackings _trackings;
}; // class sptCore::Sector

} // namespace sptCore

#endif // header guard