#ifndef SPTEDITOR_VEC3_H
#define SPTEDITOR_VEC3_H

#include "Decimal.h"
#include <cmath>

class Vec3
{
public:
    Vec3() { };
    Vec3(const Vec3& other): _x(other.getX()), _y(other.getY()), _z(other.getZ()) { };
    Vec3(const std::string& x, const std::string& y, const std::string& z): _x(x), _y(y), _z(z) { };
    Vec3(const Decimal& x, const Decimal& y, const Decimal& z): _x(x), _y(y), _z(z) { };
	
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

	void moveBy(const Vec3& other)
	{
		_x += other._x;
		_y += other._y;
		_z += other._z;
	};

	void scale(const Vec3& other)
	{
		_x *= other._x;
		_y *= other._y;
		_z *= other._z;
	};

	Decimal getX() const { return _x; }
	Decimal getY() const { return _y; }
	Decimal getZ() const { return _z; }

	void setX(const Decimal& x) { _x = x; }
	void setY(const Decimal& y) { _y = y; }
	void setZ(const Decimal& z) { _z = z; }

	float length() const
	{
		return std::sqrt(float(_x * _x + _y * _y + _z * _z));
	};
    
    float dotProduct(const Vec3& other) const
    {
        return float(_x * other._x + _y * other._y + _z * other._z);
    };

	void normalize();
	float angleToJUnit() const;

	std::string __repr__() const;

private:
	Decimal _x;
	Decimal _y;
	Decimal _z;
}; // class Vec3

#endif // header guard
