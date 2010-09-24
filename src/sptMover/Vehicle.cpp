#include <sptMover/Vehicle.h>

#include <boost/format.hpp>

using namespace boost;
using namespace sptCore;

namespace sptMover
{

void VehicleState::setLoad(float load)
{
    if(load > owner().getTraits().maxLoad)
        throw std::runtime_error(str(format("Trying to load %d on vehicle \"%s\" when only %d is allowed.") % load % owner().getName() % owner().getTraits().maxLoad));

    _load = load;
}; // sptMover::Vehicle::setLoad

float VehicleState::getTotalMass() const
{
    return owner().getTraits().mass + _load;
}; // sptMover::Vehicle::getTotalMass

Vehicle& VehicleState::owner() { 
    return reinterpret_cast<Vehicle&>(*(this - offsetof(Vehicle, state))); 
};

const Vehicle& VehicleState::owner() const { 
    return reinterpret_cast<const Vehicle&>(*(this - offsetof(Vehicle, state))); 
};

Vehicle::Vehicle(const std::string& name, const VehicleTraits& traits, Track& track, float distance): 
    _name(name), _traits(traits)
{
    for(VehicleTraits::Boogeys::const_iterator iter = getTraits().boogeys.begin(); iter != getTraits().boogeys.end(); iter++)
    {
        // put follower on track
        std::auto_ptr<Follower> follower(new Follower(track, distance + iter->distance));
        // register
        _followers.push_back(follower);
    };
}; // sptMover::Vehicle::Vehicle

void Vehicle::move(float distance)
{
    for(Followers::iterator iter = _followers.begin(); iter != _followers.end(); iter++)
    {
        iter->move(distance);
    };
}; // sptMover::Vehicle::move

}; // namespace sptMover
