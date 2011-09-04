m#ifndef SPTCORE_FOLLOWER_H
#define SPTCORE_FOLLOWER_H 1

#include <stdexcept>
#include <osg/Matrix>

#include <sptCore/Track.h>
#include <sptCore/Sector.h>
#include <sptCore/Scenery.h>

namespace sptCore
{

//! \brief Follower tied and moving on RailTracking in Scenery
//! \author Zbyszek "ShaXbee" Mandziejewicz
class Follower
{

public:
    Follower(Track& track, float distance = 0.0f);

    Sector& getSector() { return _track->getSector(); }
    const Sector& getSector() const { return _track->getSector(); }

    const RailTracking& getTrack() const { return *_track; }
    const Path& getPath() const { return *_path; }

    //! \brief Get distance from begin of current Path
    float getDistance() const { return _distance; }

    //! \brief Move follower by given distance
    //! \throw NullTrackException if there isn't next track
    void move(float distance);

    osg::Vec3 getPosition() const;
    osg::Matrix getMatrix() const;

    //! \brief Indicator of Follower exiting tracks
    class NullTrackException: public std::runtime_error { };

private:
    void changeTrack(osg::Vec3 position);
    void findPosition(osg::ref_ptr<osg::Vec3Array> points, osg::Vec3Array::const_iterator& iter, float& ratio) const;

    const RailTracking* _track;
    std::auto_ptr<const Path> _path;

    float _distance;

}; // class sptCore::Follower

}; // namespace sptCore

#endif // headerguard
