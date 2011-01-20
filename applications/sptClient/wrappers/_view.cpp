#include <boost/python.hpp>
#include <view/VehicleView.h>

using namespace boost::python;
using namespace sptMover;
using namespace view;

namespace
{

class VehicleViewComponentWrapper: public VehicleViewComponent, public wrapper<VehicleViewComponent>
{
public:
    VehicleViewComponentWrapper(const Vehicle& vehicle, const std::string& name, unsigned int updateLevel):
        VehicleViewComponent(vehicle, name, updateLevel) { };

    virtual ~VehicleViewComponentWrapper() {};
    virtual void update(float time) { get_override("update")(); };
    virtual void attach(osg::Node* model) { get_override("attach")(model); };
};

};

BOOST_PYTHON_MODULE(_view)
{
    class_<VehicleViewComponentWrapper, std::auto_ptr<VehicleViewComponent>, boost::noncopyable>("VehicleViewComponent", init<const Vehicle&, const std::string&, unsigned int>())
        .def("getName", &VehicleViewComponent::getName, return_value_policy<copy_const_reference>())
        .def("getUpdateLevel", &VehicleViewComponent::getUpdateLevel)
        .def("update", &VehicleViewComponentWrapper::update)
        .def("attach", &VehicleViewComponentWrapper::attach);

    class_<VehicleView, boost::noncopyable>("VehicleView", no_init)
        .def("addComponent", &VehicleView::addComponent)
        .def("getComponent", &VehicleView::getComponent)
        .def("hasComponent", &VehicleView::hasComponent)
        .def("getModel", &VehicleView::getModel)
        .def("getUpdateLevel", &VehicleView::getUpdateLevel)
        .def("setUpdateLevel", &VehicleView::setUpdateLevel);
    
}; // _view module