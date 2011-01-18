#include <boost/python.hpp>

#include <view/Components.h>
#include <view/VehicleView.h>

using namespace boost::python;
using namespace view;

namespace components
{
 
    struct VehicleViewComponentWrapper: public wrapper<VehicleViewComponent>
    {
        void update(float time) { this->get_override("update")(time); };
        void attach(osg::Node* model) { this->get_override("attach")(model); };
    };
 
    BOOST_PYTHON_MODULE(_components)
    {
        class_<VehicleViewComponentWrapper, std::auto_ptr<VehicleViewComponent>, boost::noncopyable>("VehicleViewComponent", init<const sptMover::Vehicle&, const std::string&, unsigned int>())
            .def("getName", &VehicleViewComponent::getName, return_value_policy<copy_const_reference>())
            .def("getUpdateLevel", &VehicleViewComponent::getUpdateLevel)
            .def("update", &VehicleViewComponentWrapper::update)
            .def("attach", &VehicleViewComponentWrapper::attach);

        class_<Body, std::auto_ptr<Body> >("Body", init<const sptMover::Vehicle&, unsigned int>())
            .def("update", &Body::update)
            .def("attach", &Body::attach);

        class_<Bogie, std::auto_ptr<Bogie> >("Bogie", init<const sptMover::Vehicle&, unsigned int, unsigned int>())
            .def("update", &Bogie::update)
            .def("attach", &Bogie::attach);
            
    }

};