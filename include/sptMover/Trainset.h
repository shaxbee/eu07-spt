#ifndef SPTMOVER_TRAINSET_H
#define SPTMOVER_TRAINSET_H 1

#include <boost/ptr_deque/ptr_vector.hpp>

#include <sptCore/RailTracking.h>
#include <sptMover/Vehicle.h>

namespace sptMover
{

class Trainset
{

public:
    Trainset(sptCore::RailTracking& track, float position = 0.0f);

    //! \brief Update trainset vehicles
    //! \param time Time passed since last update
    //! \return Distance travelled
    float update(float time);

    //! \brief Get first occupied tracking 
    const sptCore::RailTracking& getFirstTracking() const;

    //! \brief Get last occupied tracking
    const sptCore::RailTracking& getLastTracking() const;

    //! \brief Get trainset distance realtive to first tracking
    float getDistance() const;

    //! \brief Get trainset middle position
    osg::Vec3f getPosition() const;

    //! \brief Get box bounding all trainset vehicles;
    osg::BoundingBox getBoundingBox() const;

    //! \brief Get trainset speed
    float getSpeed() const;

    typedef boost::ptr_deque<Vehicle> Vehicles;
    Vehicles& getVehicles() { return _vehicles; }
    const Vehicles& getVehicles() { return _vehicles; }
    
    //! \brief Split trainset into two trainsets
    //! \param index Index of Vehicle from which split starts
    std::auto_ptr<Trainset> split(size_t index);
    
    //! \brief Join with other trainset
    //! \param other Other trainset - will be deleted after joinf
    void join(std::auto_ptr<Trainset> other);

private:
    Vehicles _vehicles;
    float _speed;

    const sptCore::Follower& getFirstFollower() const;
    const sptCore::Follower& getLastFollower() const;
    
    void checkEmpty(const char* kind) const;

}; // class sptMover::Trainset

}; // namespace sptMover

#endif // header guard