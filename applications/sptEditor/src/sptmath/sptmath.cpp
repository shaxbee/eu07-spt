#include "boost/python.hpp"

#include "Decimal.h"
#include "Vec3.h"

namespace
{

double dotProduct(const Vec3& left, const Vec3& right)
{
    return left.dotProduct(right);
};

struct DecimalPickle: boost::python::pickle_suite
{
    static boost::python::tuple getinitargs(const Decimal& value)
    {
        return boost::python::make_tuple(value.__str__());
    };
};

struct Vec3Pickle: boost::python::pickle_suite
{
    static boost::python::tuple getinitargs(const Vec3& value)
    {
        return value.to_tuple();
    };
}; // Vec3Pickle

};

#ifdef DEBUG
BOOST_PYTHON_MODULE(_sptmathd)
#else
BOOST_PYTHON_MODULE(_sptmath)
#endif
{
    using namespace boost::python;

    // show user-defined docstrings and python signatures
    docstring_options doc_options(true, false, false);

    Decimal (Decimal::*decimal_sub_operator_ptr)(const Decimal&) const = &Decimal::operator-;
    Decimal (Decimal::*decimal_neg_operator_ptr)() const = &Decimal::operator-;

    class_<Decimal>("Decimal", init<std::string>())
        .def(init<>())
        .def(init<float>())

        .def_pickle(DecimalPickle())

        .def("__float__", &Decimal::operator double)
        .def(self + self)
        .def(self - self)
        .def(self * self)
		.def(self * double())
        .def(self / self)
        .def(self == self)
        .def(-self)
		.def(!self)

        .def("__repr__", &Decimal::__repr__)
        .def("__str__",  &Decimal::__str__)

        .def("__hash__", &Decimal::hash)
        .def("compareTo",  &Decimal::compareTo, arg("other"))

        .def("to_ceiling", &Decimal::to_ceiling)
        .def("to_floor", &Decimal::to_floor)

        .def("base", &Decimal::base)
        .def("raw", &Decimal::raw);

    Vec3 (Vec3::*vec3_sub_operator_ptr)(const Vec3&) const = &Vec3::operator-;
    Vec3 (Vec3::*vec3_neg_operator_ptr)() const = &Vec3::operator-;

    class_<Vec3>("Vec3", init<>())
        .def(init<const std::string&, const std::string&, const std::string&>())
        .def(init<const Decimal&, const Decimal&, const Decimal&>())
        .def(init<const boost::int64_t, const boost::int64_t, const boost::int64_t>())
        .def(init<const Vec3&>())

        .def_pickle(Vec3Pickle())

        .add_property("x",   &Vec3::getX, &Vec3::setX)
        .add_property("y",   &Vec3::getY, &Vec3::setY)
        .add_property("z",   &Vec3::getZ, &Vec3::setZ)

        .def(self + self)
        .def(self - self)
        .def(-self)
        .def(self == self)

        .def("__hash__",     &Vec3::hash)
        .def("__repr__",     &Vec3::__repr__)

        .def("to_tuple",     &Vec3::to_tuple)
        .def("moveBy",       &Vec3::moveBy, arg("other"))
        .def("scaled",        &Vec3::scaled, arg("s"))
        .def("length",       &Vec3::length, "The length of the vector.")
        .def("dotProduct",   &Vec3::dotProduct, "Dot product of this vector and another.")
        .def("normalized",    &Vec3::normalized)
        .def("angleToJUnit", &Vec3::angleToJUnit);

    def("dotProduct", &dotProduct, args("left", "right"), "Dot product of two vectors.");

};
