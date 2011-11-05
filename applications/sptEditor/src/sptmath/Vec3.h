#ifndef SPTEDITOR_VEC3_H
#define SPTEDITOR_VEC3_H

#include "Decimal.h"
#include <cmath>
#include <boost/python/tuple.hpp>


class Vec3
{
public:
    Vec3() { };
    Vec3(const Vec3& other): _x(other.getX()), _y(other.getY()), _z(other.getZ()) { };
    Vec3(const std::string& x, const std::string& y, const std::string& z): _x(x), _y(y), _z(z) { };
    Vec3(const Decimal& x, const Decimal& y, const Decimal& z): _x(x), _y(y), _z(z) { };
    Vec3(const boost::int64_t x, const boost::int64_t y, const boost::int64_t z): _x(x), _y(y), _z(z) { };

    Vec3 operator+(const Vec3& other) const
    {
        return Vec3(_x + other._x, _y + other._y, _z + other._z);
    };

    Vec3 operator-() const
    {
        return Vec3(-_x, -_y, -_z);
    };

    Vec3 operator-(const Vec3& other) const
    {
        return Vec3(_x - other._x, _y - other._y, _z - other._z);
    };

    bool operator==(const Vec3& other) const
    {
        return (_x == other._x) && (_y == other._y) && (_z == other._z);
    };

    boost::int32_t hash() const;

    void moveBy(const Vec3& other)
    {
        _x += other._x;
        _y += other._y;
        _z += other._z;
    };

    Vec3 scaled(double value)
    {
        return scale_dec(Decimal(value));
    };

    Decimal getX() const { return _x; }
    Decimal getY() const { return _y; }
    Decimal getZ() const { return _z; }

    void setX(const Decimal& x) { _x = x; }
    void setY(const Decimal& y) { _y = y; }
    void setZ(const Decimal& z) { _z = z; }

    double length() const
    {
        double x(_x);
        double y(_y);
        double z(_z);
        return std::sqrt((x * x + y * y + z * z));
    };

    double dotProduct(const Vec3& other) const
    {
        return double(_x * other._x + _y * other._y + _z * other._z);
    };

    Vec3 normalized();
    float angleToJUnit() const;

    std::string __repr__() const;
    boost::python::tuple to_tuple() const
    {
        return boost::python::make_tuple(_x, _y, _z);
    };

private:
    Vec3 scale_dec(const Decimal& value)
    {
        return Vec3(_x * value, _y * value, _z * value);
    };

    Decimal _x;
    Decimal _y;
    Decimal _z;
}; // class Vec3

#endif // header guard
