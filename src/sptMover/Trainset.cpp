#include <sptMover/Trainset.h>

#include <boost/format.hpp>

using namespace boost;

namespace sptMover
{

Trainset::Trainset(const std::string& name):
	_name(name) 
{
};

void Trainset::setPlacement(sptCore::Track& track, float distance)
{
    for(TrainsetState::Vehicles::reverse_iterator iter = _state.vehicles.rbegin(); iter != _state.vehicles.rend(); iter++)
    {
        iter->place(track, distance);
        distance += iter->getTraits().getDimensions().x();
    };
};

bool Trainset::isPlaced() const
{
    return !_state.vehicles.empty() && _state.vehicles.front().isPlaced();
};

float Trainset::update(float time)
{
    if(!_update.get())
        return 0.0f;

    return _update->update(time, _state);

};

# if 0
    double totalForce = 0.0f;
    double totalMass = 0.0f;
    
    for(TrainsetState::Vehicles::iterator iter = _state.vehicles.begin(); iter != _state.vehicles.end(); iter++)
    {
        totalForce += iter->update(time);
        totalMass += iter->getState().getLoad() + iter->getTraits().mass;
    };
    
    _state.acceleration = totalForce / totalMass;
    double distance = (_speed + (_state.acceleration / 2 * time)) * time;
    _state.speed += _state.acceleration * time;    
    
    for(Vehicles::iterator iter = _state.vehicles.begin(); iter != _state.vehicles.end(); iter++)
    {
        iter->move(distance);
    };

	return distance;
}; // sptMover::Trainset::update
#endif

float Trainset::getDistance() const
{
    checkEmpty("distance");
    return getFirstFollower().getDistance();
}; // sptMover::Trainset::getDistance

osg::Vec3f Trainset::getPosition() const
{  
    checkEmpty("position");
    return getBoundingBox().center();
}; // sptMover::Trainset::getPosition

osg::BoundingBox Trainset::getBoundingBox() const
{
    checkEmpty("bounding box");
    return osg::BoundingBox(getFirstFollower().getPosition(), getLastFollower().getPosition());
}; // sptMover::Trainset::getBoundingBox

const sptCore::Follower& Trainset::getFirstFollower() const
{
    return *(_state.vehicles.begin()->getFollowers().begin());    
};

const sptCore::Follower& Trainset::getLastFollower() const
{
    return *(_state.vehicles.rbegin()->getFollowers().rbegin());
};

void Trainset::addVehicle(std::auto_ptr<sptMover::Vehicle> vehicle)
{
    _state.length += vehicle->getTraits().getDimensions().x();
    _state.vehicles.push_back(vehicle);
};
    
void Trainset::checkEmpty(const char* kind) const
{
    if(_state.vehicles.empty())
        throw std::logic_error(str(format("Unable to get %s of empty trainset \"%s\"") % kind % getName()));
}; // sptMover::Trainset::checkTrainsetEmpty

}; // namespace sptMover
