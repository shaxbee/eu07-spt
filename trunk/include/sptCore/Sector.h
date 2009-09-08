#ifndef SPTCORE_SECTOR_H
#define SPTCORE_SECTOR_H

#include <map>

#include <boost/exception.hpp>

#include <osg/Vec3>
#include <osg/ref_ptr>

namespace sptCore
{

class RailTracking;

class Sector
{

public:
    Sector(osg::Vec3 position): _position(position) { };

    osg::Vec3 getPosition() const { return _position; };

    //! \brief Get other track connected at given position
    //! \return Track pointer if found, NULL otherwise
    //! \throw UnknownConnectionException if there is no connection at given position
    virtual RailTracking* getNextTrack(const osg::Vec3& position, RailTracking* from) const = 0;

    typedef std::pair<RailTracking*, RailTracking*> Connection;

    //! \brief Get tracks connected at given position
    //! \warning If there is only one track at given position second entry will be NULL
    //! \throw UnknownConnectionException if there is no connection at given position
    virtual Connection getConnection(const osg::Vec3& position) const = 0;

    typedef boost::error_info<struct tag_position, osg::Vec3f> PositionInfo;
    class UnknownConnectionException: public boost::exception { };

private:
    osg::Vec3 _position;

}; // class sptCore::Sector

} // namespace sptCore

#endif // headerguard
