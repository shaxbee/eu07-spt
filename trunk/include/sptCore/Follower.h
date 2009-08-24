#ifndef SPTCORE_FOLLOWER_H
#define SPTCORE_FOLLOWER_H 1

namespace sptCore
{

class Follower
{

public:
    Follower(RailTracking* track): _track(track) { };
    virtual RailTracking* getTrack() const { return _track; } 

private:
    osg::ref_ptr<RailTracking> _track;

}; // class sptCore::Follower

}; // namespace sptCore

#endif // headerguard
