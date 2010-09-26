#ifndef SPT_VEHICLEVIEW_H
#define SPT_VEHICLEVIEW_H 1

#include <osg/Node>
#include <osg/Group>
#include <osg/MatrixTransform>

#include <sptMover/Vehicle.h>

class VehicleView: public osg::Node
{

public:
    VehicleView(sptMover::Vehicle& vehicle, osg::Group* model);

    enum AnimatedElements
    {
        ANIMATE_NOTHING = 0,
        ANIMATE_BODY = 1,
        ANIMATE_BOOGEYS = 2,
        ANIMATE_AXLES = 4
    };

    Vehicle& getVehicle() { return _vehicle; };
    const Vehicle& getVehicle() const { return _vehicle; };

    size_t getAnimatedElements() const { return _elements; };
    void setAnimatedElements(size_t elements) { _elements = elements; };

    osg::MatrixTransform* getNode() const { return _model.get(); }
    void update();

private:
    //! \brief Clone model and gather transforms
    virtual void setModel(osg::Group* model);

    // animated elements flags
    size_t _elements;
    sptMover::Vehicle& _vehicle;

    osg::ref_ptr<osg::MatrixTransform> _model;
    osg::ref_ptr<osg::Group> _boogeys;
    osg::ref_ptr<osg::Group> _axles;

}; // class spt::VehicleView

#endif // header guard
