#include <sptMover/Vehicle.h>

#include <boost/format.hpp>

using namespace boost;
using namespace sptCore;

namespace sptMover
{

VehicleUpdateCallback::~VehicleUpdateCallback() { };

Vehicle::Vehicle(const std::string& name, const VehicleTraits& traits): 
    _name(name), _traits(traits)
{
  
}; // sptMover::Vehicle::Vehicle

Vehicle::~Vehicle() { }

void Vehicle::setPlacement(Track& track, float distance)
{
    _followers.clear();

    for(VehicleTraits::Bogies::const_iterator iter = getTraits().bogies.begin(); iter != getTraits().bogies.end(); iter++)
    {
        // put follower on track
        std::auto_ptr<Follower> follower(new Follower(track, distance + iter->distance));
        // register
        _followers.push_back(follower);
    };
};

void Vehicle::move(float distance)
{
    for(Followers::iterator iter = _followers.begin(); iter != _followers.end(); iter++)
    {
        iter->move(distance);
    };
}; // sptMover::Vehicle::move

}; // namespace sptMover
