#ifndef SPTMOVER_TRAINSET_H
#define SPTMOVER_TRAINSET_H 1

#include <memory>
#include <sptCore/RailTracking.h>

namespace sptMover
{

class Vehicle;

class Trainset
{

public:
    Trainset(sptCore::RailTracking& track, float position = 0.0f);

    virtual void update(float time);

    virtual sptCore::RailTracking* getTrack() const;
    virtual float getPosition() const;
    virtual float getSpeed() const;

    virtual void addVehicle(std::auto_ptr<Vehicle> vehicle);
//    virtual std::auto_ptr<Trainset> split(Vehicle& from);

}; // class sptMover::Trainset

}; // namespace sptMover

#endif // header guard
