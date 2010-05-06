#ifndef SPT_VEHICLEVIEW_H
#define SPT_VEHICLEVIEW_H 1

#include <vector>
#include <osg/Group>
#include <osg/MatrixTransform>

#include <sptMover/Vehicle.h>

namespace spt
{

class VehicleView
{

public:
    VehicleView(const sptMover::Vehicle& vehicle, osg::Group* model): _vehicle(vehicle) { setModel(model); }

    osg::MatrixTransform* getNode() const { return _body.get(); }
    void update();

private:
    typedef std::vector<osg::ref_ptr<osg::MatrixTransform> > Nodes;

    //! \brief Clone model and gather transforms
    virtual void setModel(osg::Group* model);

    const sptMover::Vehicle& _vehicle;

    osg::ref_ptr<osg::MatrixTransform> _body;
    Nodes _boogeys;
    Nodes _axles;

}; // class spt::VehicleView

}; // namespace spt

#endif // header guard
