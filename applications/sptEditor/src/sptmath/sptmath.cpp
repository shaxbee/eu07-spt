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
};

float dotProduct(const FastVec3& left, const FastVec3& right)
{
    return left.dotProduct(right);
};

BOOST_PYTHON_MODULE(_sptmath)
{
	using namespace boost::python;

    docstring_options doc_options(true, false);
//    doc_options.disable_all();
//    doc_options.enable_user_defined();

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

//        .def("__str__",      &FastVec3::__str__)
        .def("__repr__",     &FastVec3::__repr__)

        .def("moveBy",       &FastVec3::moveBy, arg("other"))//, doc_Vec3_moveBy)
        .def("scale",        &FastVec3::scale)
        .def("length",       &FastVec3::length)
        .def("dotProduct",   &FastVec3::dotProduct)
        .def("normalize",    &FastVec3::normalize)
        .def("angleToJUnit", &FastVec3::angleToJUnit);
        
    def("dotProduct", &dotProduct);

};
