#ifndef SPT_VEHICLEVIEW_H
#define SPT_VEHICLEVIEW_H 1

#include <osg/Node>
#include <osg/Group>
#include <osg/MatrixTransform>
#include <sptMover/Vehicle.h>

class VehicleView: public osg::Node
{

public:
    VehicleView(const sptMover::Vehicle& vehicle, osg::Group* model): _vehicle(vehicle) { setModel(model); }

    osg::MatrixTransform* getNode() const { return _model.get(); }
    void update();

private:
    //! \brief Clone model and gather transforms
    virtual void setModel(osg::Group* model);

    const sptMover::Vehicle& _vehicle;

    osg::ref_ptr<osg::MatrixTransform> _model;
    osg::ref_ptr<osg::Group> _boogeys;
    osg::ref_ptr<osg::Group> _axles;

}; // class spt::VehicleView

#endif // header guard