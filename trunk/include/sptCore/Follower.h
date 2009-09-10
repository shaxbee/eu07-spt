#ifndef SPTCORE_FOLLOWER_H
#define SPTCORE_FOLLOWER_H 1

#include <boost/exception.hpp>
#include <boost/shared_ptr.hpp>

namespace sptCore
{
	
class RailTracking;
class Sector;

class Follower
{

public:
    Follower(Sector* sector, Track* track, float distance = 0.0f);

    Sector* getSector() const { return _sector.get(); }    
    RailTracking* getTrack() const { return _track.get(); }
    Path* getPath() const { return _path.get(); }

    //! \brief Get distance from begin of current Path
    float getDistance() const { return _distance; }
    
    //! \brief Move follower by given distance
    //! \throw NullTrackException if there isn't next track
    void move(float distance);
    
    class NullTrackException: public boost::exception { };
    
protected:
    virtual void setSector(Sector* sector) { _sector(sector); }

private:
	boost::shared_ptr<Sector> _sector;
	boost::shared_ptr<RailTracking> _track;

    float _distance;
    boost::shared_ptr<Path> _path;

}; // class sptCore::Follower

}; // namespace sptCore

#endif // headerguard