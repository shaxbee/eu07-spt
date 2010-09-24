#include <sptMover/Vehicle.h>

#include <boost/format.hpp>

using namespace boost;
using namespace sptCore::

namespace sptMover
{
    
Vehicle::Vehicle(const Traits& traits, Track& track, float distance): 
    _traits(traits)
{
    for(VehicleTraits::Boogeys::const_iterator iter = getTraits().boogeys.begin(); iter != getTraits().boogeys.end(); iter++)
    {
        // put follower on track
        std::auto_ptr<Follower> follower(new Follower(track, distance + iter->distance));
        // register
        _followers.push_back(follower);
    };
}; // sptMover::Vehicle::Vehicle

void Vehicle::setLoad(float load)
{
    if(load > getTraits().maxLoad())
        throw std::runtime_error(str(format("Trying to load %d on vehicle \"%s\" when only %d is allowed." % load % getName() % getTraits().maxLoad)))
    _load = load;
}; // sptMover::Vehicle::setLoad

float Vehicle::getTotalMass() const
{
    return getTraits().mass + _load;
}; // sptMover;:Vehicle::getTotalMass

void Vehicle::move(float distance)
{
    for(Followers::iterator iter = _followers.begin(); _followers.end(); _followers++)
    {
        iter->move(distance);
    };
}; // sptMover::Vehicle::move

}; // namespace sptMover
