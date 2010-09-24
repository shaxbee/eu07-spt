#include <sptMover/Trainset.h>

namespace sptMover
{

float Trainset::update(float time)
{
    double totalForce = 0.0f;
    double totalMass = 0.0f;
    
    for(Vehicles::iterator iter = _vehicles.begin(); iter != _vehicles.end(); iter++)
    {
        totalForce += iter->update(time);
        totalMass += iter->getTotalMass();
    };
    
    double acceleration = totalForce / totalMass;
    double distance = (_speed + (_acceleration / 2 * time)) * time;
    _speed += acceleration * time;    
    
    for(Vehicles::iterator iter = _vehicles.begin(); iter != _vehicles.end(); iter++)
    {
        iter->move(distance);
    };
}; // sptMover::Trainset::update

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

const sptCore::Follower& getFirstFollower() const
{
    return *(_vehicles.begin()->getFollowers().begin());    
};

const sptCore::Follower& getLastFollower() const
{
    return *(_vehicles.rbegin()->getFollowers().rbegin());
};
    
void Trainset::checkEmpty(const char* kind) const
{
    if(_vehicles.empty())
        throw std::logic_error(str(format("Unable to get %s of empty trainset \"%s\"") % kind, getName()));
}; // sptMover::Trainset::checkTrainsetEmpty

}; // namespace sptMover