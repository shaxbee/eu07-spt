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
    //! Update Vehicle state
    //! \param time period since last update
    //! \return force in N
    virtual double update(double time);

    //! Get trainset containing Vehicle
    virtual Trainset* getTrainset();

    enum Visibility
    {
        INVISIBLE,
        VISIBLE_DISTANT,
        VISIBLE_CLOSE
    };

    enum Control
    {
        NO_CONTROL,
        AI_CONTROL,
        USER_CONTROL
    };

    virtual void setVisibility(Visibility visibility);
    virtual Mode getVisibility() const;

    virtual void setControl(Control control);
    virtual Control getControl() const;

    typedef boost::error_info<struct tag_mode, Control> ControlInfo;
    class InvalidControlException: public boost::exception { };

}; // class sptMover::Vehicle

}; // namespace sptMover

#endif // header guard
