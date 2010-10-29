#include <boost/python.hpp>
#include <boost/python/stl_iterator.hpp>

#include <sptMover/Vehicle.h>

using namespace boost;
using namespace boost::python;
using namespace sptMover;

struct VehicleUpdateCallbackWrapper: VehicleUpdateCallback, wrapper<VehicleUpdateCallback>
{
    VehicleUpdateCallbackWrapper(Vehicle& vehicle): VehicleUpdateCallback(vehicle) { };
    VehicleUpdateCallbackWrapper(const VehicleUpdateCallback& source): VehicleUpdateCallback(source) { };

    virtual ~VehicleUpdateCallbackWrapper() { };
    virtual float update(float time, VehicleState& state) { get_override("update")(time, state); }
};

struct VehicleTraitsWrapper: VehicleTraits, wrapper<VehicleTraits>
{
    VehicleTraitsWrapper() { };
    VehicleTraitsWrapper(const VehicleTraits& source): VehicleTraits(source) { };

    list* getBogies() const
    {
        return new list(VehicleTraits::getBogies());
    };

    void setBogies(list bogies)
    {
        stl_input_iterator<float> begin(bogies), end;
        Bogies vec(begin, end);
        VehicleTraits::setBogies(vec);
    };
};

BOOST_PYTHON_MODULE(_sptMover)
{

    class_<VehicleTraitsWrapper>("VehicleTraits")
        .add_property("dimensions", make_function(&VehicleTraits::getDimensions, return_value_policy<return_by_value>()), &VehicleTraits::setDimensions)
        .add_property("mass", &VehicleTraits::getMass, &VehicleTraits::setMass)
        .add_property("maxLoad", &VehicleTraits::getMaxLoad, &VehicleTraits::setMaxLoad)
        .add_property("bogies", make_function(&VehicleTraitsWrapper::getBogies, return_value_policy<manage_new_object>()), &VehicleTraitsWrapper::setBogies);

    class_<VehicleState>("VehicleState")
        .add_property("load", &VehicleState::getLoad, &VehicleState::setLoad);

    class_<VehicleUpdateCallbackWrapper>("VehicleUpdateCallback", init<Vehicle&>())
        .def("update",     &VehicleUpdateCallbackWrapper::update, args("time", "state"))
        .def("getVehicle", &VehicleUpdateCallback::getVehicle, return_value_policy<reference_existing_object>());

    class_<Vehicle, noncopyable>("Vehicle", init<const std::string&, const VehicleTraits&>())
        .def("place",     &Vehicle::place, args("track", "distance"))
        .def("isPlaced",  &Vehicle::isPlaced)

        .def("setUpdateCallback", &Vehicle::setUpdateCallback, args("callback"))

        .def("update",    &Vehicle::update, args("time"))
        .def("move",      &Vehicle::move, args("distance"))

        .def("getName",   &Vehicle::getName, return_value_policy<return_by_value>()) 
        .def("getTraits", &Vehicle::getTraits, return_value_policy<return_by_value>())
        .def("getState",  &Vehicle::getState, return_value_policy<return_by_value>());

};
