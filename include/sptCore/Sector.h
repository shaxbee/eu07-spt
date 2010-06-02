#ifndef SPTCORE_SECTOR_H
#define SPTCORE_SECTOR_H

#include <map>

#include <boost/exception.hpp>
#include <boost/noncopyable.hpp>

#include <osg/Vec3>
#include <osg/ref_ptr>

#include <sptCore/RailTracking.h>

namespace sptCore
{

class Scenery;

//! \brief Bounded region of Scenery
//! Sector manages RailTracking instances and connections between them.
//! \author Zbyszek "ShaXbee" Mandziejewicz
class Sector: boost::noncopyable
{

public:
    Sector(Scenery& scenery, osg::Vec3 position): _scenery(scenery), _position(position) { };
    virtual ~Sector() { };

    static float SIZE;

    Scenery& getScenery() { return _scenery; };
    const osg::Vec3& getPosition() const { return _position; };

    //! \brief Get other track connected at given position
    //! \throw UnknownConnectionException if there is no connection at given position
    virtual const RailTracking& getNextTrack(const osg::Vec3& position, const RailTracking& from) const = 0;
    virtual size_t getTotalTracks() const = 0;

    typedef std::pair<const RailTracking*, const RailTracking*> Connection;

    //! \brief Get tracks connected at given position
    //! \throw UnknownConnectionException if there is no connection at given position
    virtual const Connection& getConnection(const osg::Vec3& position) const = 0;

    typedef boost::error_info<struct tag_position, osg::Vec3f> PositionInfo;
    class UnknownConnectionException: public boost::exception { };

private:
    Scenery& _scenery;
    osg::Vec3 _position;

}; // class sptCore::Sector

} // namespace sptCore

#endif // headerguard
