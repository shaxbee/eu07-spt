#ifndef SPTEDITOR_FASTDEC_H
#define SPTEDITOR_FASTDEC_H

#include "FastDec.h"

class FastVec3
{
public:
	explicit FastVec3(FastDec x, FastDec y, FastDec z): _x(x), _y(y), _z(z) { };
	
	FastVec3 operator+(const FastVec3& other) const
	{
		return FastVec3(_x + other._x, _y + other._y, _z + other._z);
	};

	FastVec3 operator-(const FastVec3& other) const
	{
		return FastVec3(_x - other._x, _y - other._y, _z - other._z);
	};

	FastVec3& operator+=(const FastVec3& other)
	{
		_x += other._x;
		_y += other._y;
		_z += other._z;
		return *this;
	};

	FastVec3& operator*=(const FastVec3& other)
	{
		_x *= other._x;
		_y *= other._y;
		_z *= other._z;
		return *this;
	};

	const FastDec& getX() const { return _x; }
	const FastDec& getY() const { return _y; }
	const FastDec& getZ() const { return _z; }

	void setX(const FastDec& x) { _x = x; }
	void setY(const FastDec& y) { _y = y; }
	void setZ(const FastDec& z) { _z = z; }

	float length() const
	{
		std::sqrt(_x * _x + _y * _y + _z * _z);
	};

	void normalize();
	float angleToJUnit() const;

	std::string repr() const;

private:
	FastDec _x;
	FastDec _y;
	FastDec _z;
}; // class FastVec3

#endif // header guard
