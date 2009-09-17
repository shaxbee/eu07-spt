#ifndef SPTMOVER_TRAINSET_H
#define SPTMOVER_TRAINSET_H 1

namespace sptMover
{

class Trainset: public Mover
{

public:
    Trainset(sptCore::RailTracking* track, float offset = 0.0f);

    virtual void update(float time);

    virtual sptCore::RailTracking* getTrack() const;
    virtual float getOffset() const;
    virtual float getSpeed() const;

    virtual void addVehicle(Vehicle* vehicle);
    virtual Trainset* split(Vehicle* from);

}; // class sptMover::Trainset

}; // namespace sptMover

#endif // header guard
