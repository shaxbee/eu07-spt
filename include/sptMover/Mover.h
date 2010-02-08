#ifndef SPTMOVER_MOVER_H
#define SPTMOVER_MOVER_H 1

#include <sptCore/Follower.h>

namespace sptMover
{

class Mover: public sptCore::Follower
{

public:
    Mover(sptCore::RailTracking* track, float position = 0.0f): sptCore::Follower(track), _offset(offset) { };

    virtual void update(double time) = 0;

    virtual float getPosition() const { return _position; } 
    virtual float getSpeed() const = 0;
    virtual float getAcceleration() const = 0;

private:
    float _position;

}; // class sptMover::Mover

}; // namespace sptMover

#endif // header guard

