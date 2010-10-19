#ifndef SPTMOVER_VEHICLE_H
#define SPTMOVER_VEHICLE_H 1

#include <vector>
#include <boost/scoped_ptr.hpp>
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
    void setLoad(float load) { _load = load; }
    float getLoad() const { return _load; }

    float getAxleSpeed(size_t index) const { return _axleSpeeds.at(index); }
    void setAxleSpeed(size_t index, float speed) { _axleSpeeds.at(index) = speed; }

private:
    float _load;

    typedef std::vector<float> AxleSpeeds;
    AxleSpeeds _axleSpeeds;
};

class VehicleUpdateCallback
{
public:
    VehicleUpdateCallback(Vehicle& vehicle);
    virtual ~VehicleUpdateCallback();

    virtual float update(float time, VehicleState& state) = 0;

    const Vehicle& getVehicle() const { return _vehicle; }

private:
    Vehicle& _vehicle;
};

//! Vehicle represents Trainset element
class Vehicle
{

public:
	Vehicle(const std::string& name, const VehicleTraits& traits);
    ~Vehicle();

    void setPlacement(sptCore::Track& track, float distance = 0.0f);
    bool isPlaced() const { return !_followers.empty(); }

	const std::string& getName() const { return _name; }

    const VehicleUpdateCallback& getUpdateCallback() const { return *_update; }
    void setUpdateCallback(std::auto_ptr<VehicleUpdateCallback> update) { _update = update; }

    //! \brief Update vehicle state
    //! \param time period since last update
    //! \return force
    float update(float time);

    //! \brief Move vehicle by given distance
    void move(float distance);
        
	typedef boost::ptr_vector<sptCore::Follower> Followers;    
    const Followers& getFollowers() const { return _followers; }

    const VehicleTraits& getTraits() const { return _traits; }
    const VehicleState& getState() const { return _state; }

private:
	std::string _name;
    Followers _followers;

    const VehicleTraits _traits;
    VehicleState _state;

    std::auto_ptr<VehicleUpdateCallback> _update;

}; // class sptMover::Vehicle

}; // namespace sptMover

#endif // header guard
