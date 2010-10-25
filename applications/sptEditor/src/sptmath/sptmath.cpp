#include "boost/python.hpp"

#include "FastDec.h"
#include "FastVec3.h"

BOOST_PYTHON_MODULE(_sptmath)
{
	using namespace boost::python;

	class_<FastDec>("FastDec", init<std::string>())
		.def("__add__",  &FastDec::operator+)
		.def("__sub__",  &FastDec::operator-)
		.def("__mul__",  &FastDec::operator*)
		.def("__div__",  &FastDec::operator/)
		.def("__eq__",   &FastDec::operator==)
		.def("__str__",  &FastDec::str)
		.def("__repr__", &FastDec::repr);

    class_<FastVec3>("FastVec3", init<FastDec, FastDec, FastDec>())
        .add_property("x",   &FastVec3::getX, &FastVec3::setX)
        .add_property("y",   &FastVec3::getY, &FastVec3::setY)
        .add_property("z",   &FastVec3::getZ, &FastVec3::setZ)

        .def("__add__",      &FastVec3::operator+)
        .def("__sub__",      &FastVec3::operator-)
        .def("__repr__",     &FastVec3::repr)

        .def("moveBy",       &FastVec3::moveBy)
        .def("scale",        &FastVec3::scale)
        .def("length",       &FastVec3::length)
        .def("normalize",    &FastVec3::normalize)
        .def("angleToJUnit", &FastVec3::angleToJUnit);

};
