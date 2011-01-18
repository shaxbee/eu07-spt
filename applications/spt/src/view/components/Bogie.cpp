#include <boost/python.hpp>
#include <boost/format.hpp>

#include <view/Components.h>
#include <view/VehicleView.h>
#include <view/Util.h>

using namespace boost::python;

namespace components
{

Bogie::Bogie(const sptMover::Vehicle& vehicle, unsigned int index, unsigned int updateLevel):
    VehicleViewComponent(vehicle, boost::str(boost::format("bogie%02d") % index), updateLevel),
    _index(index)
{
};

void Bogie::update(float time)
{
    if(_node.valid())
    {
        const sptCore::Follower& follower = getVehicle().getFollowers().at(getIndex());
        _node->setMatrix(follower.getMatrix());
    };
};

void Bogie::attach(osg::Node* model)
{
    _node = view::injectTransform(model, getName());
};

} // namespace components