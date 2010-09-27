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
    // diameter of axle wheels
    float diameter;
};

struct VehicleBogieTraits
{
    float distance;
    // distance from center of bogie to buffers
//    float bufferDistance;
    // axles traits
    typedef std::vector<VehicleAxleTraits> Axles;
    Axles axles;
};

struct VehicleTraits
{
    // dimensions of vehicle: length, width, height
    osg::Vec3f dimensions;
    // mass of empty vehicle
    float mass;
    // maximal mass of load
    float maxLoad;
    // bogies traits
    typedef std::vector<VehicleBogieTraits> Bogies;
    Bogies bogies;
};

class VehicleState
{
public:
//F    VehicleState();

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

    //! \brief Move vehicle by given distance
    void move(float distance);
        
	typedef boost::ptr_vector<sptCore::Follower> Followers;    
    const Followers& getFollowers() const { return _followers; }

    const VehicleTraits traits;
    VehicleState state;

private:
	std::string _name;
    Followers _followers;

}; // class sptMover::Vehicle

}; // namespace sptMover

#endif // header guard
