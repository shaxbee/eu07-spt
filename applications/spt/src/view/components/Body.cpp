#include <boost/python.hpp>

#include <osg/Vec3>
#include <osg/Matrix>

#include <sptUtil/Math.h>

#include <view/Components.h>
#include <view/VehicleView.h>
#include <view/Util.h>

using namespace boost::python;

namespace components
{

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

};