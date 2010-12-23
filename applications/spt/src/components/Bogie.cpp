#include <boost/python.hpp>
#include <boost/format.hpp>

#include <view/VehicleView.h>
#include <view/Util.h>

using namespace boost::python;

namespace components
{

class Bogie: public view::VehicleViewComponent
{
public:
    Bogie(const sptMover::Vehicle& vehicle, unsigned int index, unsigned int updateLevel);

    virtual void update(float time);
    virtual void attach(osg::Node* model);

    unsigned int getIndex() const { return _index; };

private:
    osg::ref_ptr<osg::MatrixTransform> _node;
    unsigned int _index;
    
};

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

void export_bogie()
{
    class_<Bogie>("Bogie", init<const sptMover::Vehicle&, unsigned int, unsigned int>())
        .def("update", &Bogie::update)
        .def("attach", &Bogie::attach);
};

} // namespace components