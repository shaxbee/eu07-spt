#include "boost/python.hpp"

#include "FastDec.h"
#include "FastVec3.h"

namespace
{

const char* doc_Vec3 =
"A vector in 3D world.\n"
"It uses fixed decimal point coordinates. It stores three decimal places.\n"
"\n"
"Setting x, y, z causes to quantize the value to one millimetre.\n"
"\n"
"Examples:\n"
">>> Vec3('0.001', '-0.001', '0.000')\n"
"(0.001,-0.001,0.000)\n"
">>> a = Vec3('0.0001', '-0.0001', '0.000')\n"
">>> a\n"
"(0.000,0.000,0.000)\n"
">>> Vec3('0.999', '-0.999', '1.000')\n"
"(0.999,-0.999,1.000)\n"
">>> b = Vec3('0.0005', '-0.0006', '-0.0004')\n"
">>> str(b.x)\n"
"'0.001'\n"
">>> str(b.y)\n"
"'-0.001'\n"
">>> str(b.z)\n"
"'0.000'\n"
">>> a + b\n"
"(0.001,-0.001,0.000)\n"
">>> Vec3('0.9999', '-0.9999', '0.000')\n"
"(1.000,-1.000,0.000)\n"
">>> Vec3('1.0001', '0.000', '-1.0001')\n"
"(1.000,0.000,-1.000)\n"
">>> c = Vec3('0.0004', '-0.0004', '0.000')\n"
">>> c + c\n"
"(0.000,0.000,0.000)\n";

const char* doc_Vec3_eq = \
"Returns True if two Vec3 are equal.\n"
"\n"
"Note that Decimal -0.000 is equal with 0.000\n"
"\n"
"Examples:\n"
">>> Vec3('0.000', '-0.000', '0.000') == Vec3('-0.0', '0', '-0')\n"
"True\n"
">>> Vec3('1.0', '-1.0', '0.001') == Vec3('1.000', '-1', '0.001')\n"
"True\n"
">>> Vec3('2', '3', '-4.009') == Vec3('-2', '3.000', '-5')\n"
"False\n";

const char* doc_Vec3_moveBy = \
"Moves this vector by given other v vector.\n"
"\n"
"Example:\n"
">>> a = Vec3('5.67', '34.43', '-898')\n"
">>> v = Vec3('-6', '34.44', '0.0004')\n"
">>> a.moveBy(-v)\n"
">>> a\n"
"(11.670,-0.010,-898.000)\n"
">>> str(a.z)\n"
"'-898.000'\n";

const char* doc_Vec3_normalize = \
"Normalizes the vector.\n"
"\n"
"Examples:\n"
">>> Vec3('1', '0', '0').normalize()\n"
"(1.000,0.000,0.000)\n"
">>> Vec3('0', '-1', '0').normalize()\n"
"(0.000,-1.000,0.000)\n"
">>> Vec3('-1', '-1', '0').normalize()\n"
"(-0.707,-0.707,0.000)\n"
">>> Vec3('0.001', '0', '0').normalize()\n"
"(1.000,0.000,0.000)\n"
">>> Vec3('-0.001', '-0.001', '0.001').normalize()\n"
"(-0.577,-0.577,0.577)\n";

const char* doc_Vec3_angleToJUnit = \
"Returns the angle in radians to the unit vector J=(0, 1, 0).\n"
"\n"
"Examples:\n"
">>> str(Vec3('0', '1', '0').angleToJUnit())\n"
"'0.0'\n"
">>> str(Vec3('1', '0', '0').angleToJUnit())\n"
"'1.57079632679'\n"
">>> str(Vec3('-1', '0', '0').angleToJUnit())\n"
"'4.71238898038'\n"
">>> str(Vec3('0', '-1', '0').angleToJUnit())\n"
"'3.14159265359'\n"
">>> str(Vec3('1', '1', '0').angleToJUnit())\n"
"'0.785398163397'\n"
">>> str(Vec3('-1', '1', '0').angleToJUnit())\n"
"'5.49778714378'\n";

const char* doc_Vec3_scale = \
"Scales the vector by scale s.\n"
"\n"
"Examples:\n"
">>> Vec3('1', '3', '0.5').scale(2)\n"
"(2.000,6.000,1.000)\n"
">>> Vec3('-4', '0.001', '-0.999').scale(0.5)\n"
"(-2.000,0.001,-0.500)\n"
">>> Vec3('0', '7', '-3').scale(-2)\n"
"(-0.000,-14.000,6.000)\n"
">>> Vec3('5', '0.45', '-0.002').scale(0)\n"
"(0.000,0.000,-0.000)\n";

float dotProduct(const FastVec3& left, const FastVec3& right)
{
    return left.dotProduct(right);
};

};

BOOST_PYTHON_MODULE(_sptmath)
{
	using namespace boost::python;

    // show user-defined docstrings and python signatures
    docstring_options doc_options(true, true, false);

	class_<FastDec>("FastDec", init<std::string>())
		.def("__add__",  &FastDec::operator+)
		.def("__sub__",  &FastDec::operator-)
		.def("__mul__",  &FastDec::operator*)
		.def("__div__",  &FastDec::operator/)
		.def("__eq__",   &FastDec::operator==)

		.def("__repr__", &FastDec::__repr__)
		.def("__str__", &FastDec::__str__);

    class_<FastVec3>("FastVec3", doc_Vec3, init<const std::string&, const std::string&, const std::string&>(args("x", "y", "z")))
        .add_property("x",   &FastVec3::getX, &FastVec3::setX)
        .add_property("y",   &FastVec3::getY, &FastVec3::setY)
        .add_property("z",   &FastVec3::getZ, &FastVec3::setZ)

        .def("__add__",      &FastVec3::operator+)
        .def("__sub__",      &FastVec3::operator-)
        .def("__eq__",       &FastVec3::operator==, arg("other"), doc_Vec3_eq)

        .def("__repr__",     &FastVec3::__repr__)

        .def("moveBy",       &FastVec3::moveBy, arg("other"), doc_Vec3_moveBy)
        .def("scale",        &FastVec3::scale, arg("s"), doc_Vec3_scale)
        .def("length",       &FastVec3::length, "The length of the vector.")
        .def("dotProduct",   &FastVec3::dotProduct, "Dot product of this vector and another.")
        .def("normalize",    &FastVec3::normalize, doc_Vec3_normalize)
        .def("angleToJUnit", &FastVec3::angleToJUnit, doc_Vec3_angleToJUnit);
        
    def("dotProduct", &dotProduct, args("left", "right"), "Dot product of two vectors.");

};
