#ifndef SPT_TRAINSETVIEW_H
#define SPT_TRAINSETVIEW_H 1

#include <sptMover/Trainset.h>

namespace spt
{

class TrainsetView
{

public:
    TrainsetView(sptMover::Trainset& trainset);

    void update();
//    void addVehicle(osg::Group* vehicle);

private:
    typedef std::vector<VehicleView> Geometries;

    sptMover::Trainset& _trainset;
    Geometries _geometries;

}; // class spt::TrainsetView

}; // namespace spt

#endif