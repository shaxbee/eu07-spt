#ifndef SPTMOVER_VEHICLE_H
#define SPTMOVER_VEHICLE_H 1

#include <vector>

#include <sptCore/Follower.h>

namespace sptMover
{

class Trainset;
    
struct VehicleAxleTraits
{
    // distance from first axle
    float distance;
    // diameter of axle wheels
    float diameter;
};

struct VehicleBoogeyTraits
{
    // distance from front of vehicle
    float distance;
    // length of boogey - distance between first and last axle
    float length;
    // axles traits
    std::vector<VehicleAxleTraits> axles;
};

struct VehicleTraits
{
    // length of vehicle from front to back buffer
    float length;
    // mass of empty vehicle
    float mass;
    // maximal mass of load
    float maxLoad;
    // boogeys traits
    typedef std::vector<VehicleBoogeyTraits> Boogeys;
    Boogeys boogeys;
};

//! Vehicle represents Trainset element
class Vehicle
{

public:
    Vehicle(const Traits& traits, sptCore::Track& track, float distance);

    //! \brief Update Vehicle state
    //! \param time period since last update
    //! \return force
    float update(float time);
    
    void move(float distance);
    
    void setLoad(float load);
    float getLoad() const { return _load; }
    
    float getTotalMass() const;

    //! \brief Get trainset containing Vehicle
//    Trainset& getTrainset() { return *_trainset; }
//    const Trainset& getTrainset() const { return *_trainset; }
    
//    void setTrainset(Trainset& trainset) { _trainset = trainset; }

    //! \brief Get physical traits
    const VehicleTraits& getTraits() { return _traits; }
    
    typedef boost::ptr_vector<sptCore::Follower> Followers;
    
    const Followers& getFollowers() const { return _followers; }

private:
//    Trainset* _trainset;
    const VehicleTraits _traits;
    float _load;

    Followers _followers;

}; // class sptMover::Vehicle

}; // namespace sptMover

#endif // header guard
