#ifndef SPTCORE_SECTOR_H
#define SPTCORE_SECTOR_H 1

#include <vector>

#include <boost/cstdint.hpp>
#include <boost/tr1/unordered_map.hpp>
#include <boost/ptr_container/ptr_vector.hpp>

#include <osg/Vec3f>

#include "sptCore/RailTracking.h"

namespace sptCore
{

typedef boost::ptr_vector<Track> RailTrackings;

struct Connection
{
    const size_t first;
    const size_t second;
};

typedef std::tr1::unordered_map<osg::Vec3f, Connection> Connections;

//! Container for rail trackings located in chunk of Scenery
//! \author Zbigniew "ShaXbee" Mandziejewicz
class Sector
{
public:
    Sector(const osg::Vec3f& position, RailTrackings& trackings, Connections& connections);

    const osg::Vec3f& getPosition() const { return _position; };

    //! \brief Get id of other track connected at given position.
    //! \throw UnknownConnectionException if there is no connection at given position
    const size_t getNextRailTracking(const osg::Vec3f& position, const size_t from) const;

    const Track& getRailTracking(const size_t index) const;

    size_t getRailTrackingCount() const;

    typedef boost::error_info<struct tag_position, osg::Vec3f> PositionInfo;
    class UnknownConnectionException: public boost::exception { };

    static float SIZE;

private:
    const osg::Vec3f _position;
    Connections _connections;
    RailTrackings _trackings;
}; // class sptCore::Sector

} // namespace sptCore

#endif // header guard