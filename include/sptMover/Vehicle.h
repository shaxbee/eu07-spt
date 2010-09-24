#ifndef SPTMOVER_VEHICLE_H
#define SPTMOVER_VEHICLE_H 1

#include <vector>
#include <boost/ptr_container/ptr_vector.hpp>

#include <sptCore/Follower.h>

namespace sptMover
{

class Trainset;
class Vehicle;
    
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
    // distance between first and last axle - calculated automagically
    float length;
    // axles traits
    typedef std::vector<VehicleAxleTraits> Axles;
    Axles axles;
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

class VehicleState
{
public:
    VehicleState();

    void setLoad(float load);
    float getLoad() const { return _load; }
    
    float getTotalMass() const;

    float getAxleSpeed(size_t index) const { return _axleSpeeds.at(index); }
    void setAxleSpeed(size_t index, float speed) { _axleSpeeds.at(index) = speed; }

private:
    Vehicle& owner();
    const Vehicle& owner() const;

    float _load;

    typedef std::vector<float> AxleSpeeds;
    AxleSpeeds _axleSpeeds;
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
    
    //! \brief Get physical traits
    const VehicleTraits& getTraits() const { return _traits; }
    
	typedef boost::ptr_vector<sptCore::Follower> Followers;    
    const Followers& getFollowers() const { return _followers; }

    VehicleState state;

private:
//    Trainset* _trainset;
	std::string _name;
    const VehicleTraits _traits;

    Followers _followers;

}; // class sptMover::Vehicle

}; // namespace sptMover

#endif // header guard
