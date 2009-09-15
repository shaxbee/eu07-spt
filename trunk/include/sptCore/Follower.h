#ifndef SPTCORE_FOLLOWER_H
#define SPTCORE_FOLLOWER_H 1

#include <boost/exception.hpp>
#include <boost/shared_ptr.hpp>

#include <sptCore/RailTracking.h>
#include <sptCore/Sector.h>

namespace sptCore
{

class Path;    
class Track;

class Follower
{

public:
    Follower(Sector* sector, Track* track, float distance = 0.0f);

    const Sector& getSector() const { return *_sector; }    
    const RailTracking& getTrack() const { return *_track; }
    const Path& getPath() const { return *_path; }

    //! \brief Get distance from begin of current Path
    float getDistance() const { return _distance; }
    
    //! \brief Move follower by given distance
    //! \throw NullTrackException if there isn't next track
    void move(float distance);
    
    class NullTrackException: public boost::exception { };
    
protected:
    virtual void setSector(Sector* sector) { _sector = sector; }

private:
	Sector* _sector;
	RailTracking* _track;
    Path* _path;

    float _distance;

}; // class sptCore::Follower

}; // namespace sptCore

#endif // headerguard
