#include <boost/python.hpp>

#include <osg/Vec3>
#include <osg/Matrix>

#include <sptUtil/Math.h>

#include <view/VehicleView.h>
#include <view/Util.h>

using namespace boost::python;

namespace components
{

class Body: public view::VehicleViewComponent
{
public:
    Body(const sptMover::Vehicle& vehicle, unsigned int updateLevel);

    virtual void update(float time);
    virtual void attach(osg::Node* model);

private:
    osg::ref_ptr<osg::MatrixTransform> _node;
};

Body::Body(const sptMover::Vehicle& vehicle, unsigned int updateLevel):
    VehicleViewComponent(vehicle, "body", updateLevel)
{
};

void Body::update(float time)
{
    if(_node.valid())
    {
        const sptMover::Vehicle::Followers& followers = getVehicle().getFollowers();
        osg::Vec3f front = followers.front().getPosition();
        osg::Vec3f back = followers.back().getPosition();
        
        osg::Matrixf matrix = osg::Matrix::translate((front + back) / 2);
        matrix *= sptUtil::rotationMatrix(back - front);
        
        _node->setMatrix(matrix);
    };
};

void Body::attach(osg::Node* model)
{
    _node = view::injectTransform(model, getName());
};

void export_body()
{
    class_<Body>("Body", init<const sptMover::Vehicle&, unsigned int>())
        .def("update", &Body::update)
        .def("attach", &Body::attach);
};

};