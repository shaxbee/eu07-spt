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

class VehicleTraits
{
public:
    // dimensions of vehicle: length, width, height
    const osg::Vec3f& getDimensions() const { return _dimensions; }
    void setDimensions(const osg::Vec3f& dimensions) { _dimensions = dimensions; }

    // mass of empty vehicle
    float getMass() const { return _mass; }
    void setMass(float mass) { _mass = mass; }

    // maximal mass of load
    float getMaxLoad() const { return _maxLoad; }
    void setMaxLoad(float maxLoad) { _maxLoad = maxLoad; }

    // bogies distances
    typedef std::vector<float> Bogies;
    const Bogies& getBogies() const { return _bogies; }
    void setBogies(const Bogies& bogies) { _bogies = bogies; }

private:
    osg::Vec3f _dimensions;
    float _mass;
    float _maxLoad;
    Bogies _bogies;
};

class VehicleState
{
public:
    float getLoad() const { return _load; }
    void setLoad(float load) { _load = load; }

private:
    float _load;
};

class VehicleUpdateCallback
{
public:
    VehicleUpdateCallback(Vehicle& vehicle): _vehicle(vehicle) { };
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

    void place(sptCore::Track& track, float distance = 0.0f);
    bool isPlaced() const { return !_followers.empty(); }

    const std::string& getName() const { return _name; }

    bool hasUpdateCallback() const { return _update.get() != NULL; }
    VehicleUpdateCallback& getUpdateCallback();
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
