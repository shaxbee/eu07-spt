#include "boost/python.hpp"

#include "FastDec.h"
#include "FastVec3.h"

BOOST_PYTHON_MODULE(_sptmath)
{
	using namespace boost::python;

	class<FastDec>("FastDec", init<std::string>())
		.def("__add__",  &FastDec::operator+)
		.def("__sub__",  &FastDec::operator-)
		.def("__mul__",  &FastDec::operator*)
		.def("__div__",  &FastDec::operator/)
		.def("__eq__",   &FastDec::operator==)
		.def("__str__",  &FastDec::str)
		.def("__repr__", &FastDec::repr);
};
