#ifndef SPTMOVER_TRAINSET_H
#define SPTMOVER_TRAINSET_H 1

#include <string>
#include <boost/ptr_container/ptr_deque.hpp>

#include <osg/Vec3>
#include <osg/BoundingBox>

#include <sptCore/RailTracking.h>
#include <sptMover/Vehicle.h>

namespace sptMover
{

class TrainsetState
{
public:
    typedef boost::ptr_deque<Vehicle> Vehicles;
    Vehicles vehicles;

    float speed;
    float acceleration;

    float length;
};

class TrainsetUpdateCallback
{
public:
    TrainsetUpdateCallback(Trainset& trainset): _trainset(trainset) { };
    virtual ~TrainsetUpdateCallback() { };

    virtual float update(float time, TrainsetState& trainset) = 0;
    const Trainset& getTrainset() const { return _trainset; }

private:
    Trainset& _trainset;

}; // sptMover::TrainsetUpdateCallback

class Trainset
{

public:
    Trainset(const std::string& name);

    void setPlacement(sptCore::SimpleTrack& track, float distance);
    bool isPlaced() const;

    const TrainsetUpdateCallback& getUpdateCallback() const { return *_update; }
    void setUpdateCallback(std::auto_ptr<TrainsetUpdateCallback> update) { _update = update; }

    //! \brief Update trainset vehicles
    //! \param time Time passed since last update
    //! \return Distance travelled
    float update(float time);

    const std::string& getName() const { return _name; };

    //! \brief Get first occupied tracking
    const sptCore::Track& getFirstTracking() const;

    //! \brief Get last occupied tracking
    const sptCore::Track& getLastTracking() const;

    float getLength() const { return _state.length; }

    //! \brief Get trainset distance realtive to first tracking
    float getDistance() const;

    //! \brief Get trainset speed from last update
    float getSpeed() const { return _state.speed; }

    //! \brief Get trainset acceleration from last update
    float getAcceleration() const { return _state.acceleration; }

    //! \brief Get trainset middle position
    osg::Vec3f getPosition() const;

    //! \brief Get box bounding all trainset vehicles;
    osg::BoundingBox getBoundingBox() const;

    void addVehicle(std::auto_ptr<Vehicle> vehicle);

    //! \brief Split trainset into two trainsets
    //! \param index Index of Vehicle from which split starts
    std::auto_ptr<Trainset> split(size_t index);

    //! \brief Join with other trainset
    //! \param other Other trainset - will be deleted after join
    void join(std::auto_ptr<Trainset> other);

private:
    std::string _name;
    TrainsetState _state;

    std::auto_ptr<TrainsetUpdateCallback> _update;

    const sptCore::Follower& getFirstFollower() const;
    const sptCore::Follower& getLastFollower() const;

    void checkEmpty(const char* kind) const;

}; // class sptMover::Trainset

}; // namespace sptMover

#endif // header guard
