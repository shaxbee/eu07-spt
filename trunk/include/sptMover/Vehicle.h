#ifndef SPTMOVER_VEHICLE_H
#define SPTMOVER_VEHICLE_H 1

#include <boost/exception.hpp>

namespace sptMover
{

class Trainset;

//! Vehicle represents Trainset element
class Vehicle
{

public:
    typedef boost::function<double(double)> UpdateCallback;

    Vehicle(Trainset& trainset, float length, UpdateCallback callback = 0);

    //! \brief Update Vehicle state
    //! \param time period since last update
    //! \return force
    virtual double update(double time);

    //! \brief Get trainset containing Vehicle
    virtual Trainset& getTrainset() { return *_trainset; }

private:
    Trainset* _trainset;
    float _length;
    UpdateCallback _callback;

}; // class sptMover::Vehicle

}; // namespace sptMover

#endif // header guard
