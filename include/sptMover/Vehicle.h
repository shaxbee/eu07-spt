#ifndef SPTMOVER_VEHICLE_H
#define SPTMOVER_VEHICLE_H 1

#include <vector>
#include <boost/ptr_container/ptr_vector.hpp>

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
	Vehicle(const std::string& name, const VehicleTraits& traits, sptCore::Track& track, float distance = 0.0f);

	const std::string& getName() const { return _name; }

    //! \brief Update vehicle state
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
    const VehicleTraits& getTraits() const { return _traits; }
    
	typedef boost::ptr_vector<sptCore::Follower> Followers;
    
    const Followers& getFollowers() const { return _followers; }

private:
//    Trainset* _trainset;
	std::string _name;
    const VehicleTraits _traits;
    float _load;

    Followers _followers;

}; // class sptMover::Vehicle

}; // namespace sptMover

#endif // header guard
