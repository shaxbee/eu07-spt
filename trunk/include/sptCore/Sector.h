#ifndef SPTCORE_SECTOR_H
#define SPTCORE_SECTOR_H

#include <osg/Vec3>
#include <osg/ref_ptr>

namespace sptCore
{

class Sector
{

public:
    Sector(osg::Vec3d position): _position(position) { };

    osg::Vec3d getPosition() const { return _position; };

    //! \brief Get other track connected at given position
    //! \return Track pointer if found, NULL otherwise
    virtual Track* getNextTrack(const osg::Vec3& position, Track* from) const = 0;

    //! \brief Get tracks connected at given position
    //! \warning If there is only one track at given position second entry will be NULL
    virtual std::pair<Track*, Track*> getTracksAt(const osg::Vec3& position) const = 0;

private:
    osg::Vec3d _position;

} // class sptCore::Sector

} // namespace sptCore

#endif // headerguard
