#ifndef SPTEDITOR_FASTVEC3_H
#define SPTEDITOR_FASTVEC3_H

#include "FastDec.h"

class FastVec3
{
public:
//	explicit ;
    FastVec3(const std::string& x, const std::string& y, const std::string& z): _x(x), _y(y), _z(z) { };
	
	FastVec3 operator+(const FastVec3& other) const
	{
		return FastVec3(_x + other._x, _y + other._y, _z + other._z);
	};

	FastVec3 operator-(const FastVec3& other) const
	{
		return FastVec3(_x - other._x, _y - other._y, _z - other._z);
	};

	void moveBy(const FastVec3& other)
	{
		_x += other._x;
		_y += other._y;
		_z += other._z;
	};

	void scale(const FastVec3& other)
	{
		_x *= other._x;
		_y *= other._y;
		_z *= other._z;
	};

	FastDec getX() const { return _x; }
	FastDec getY() const { return _y; }
	FastDec getZ() const { return _z; }

	void setX(const FastDec& x) { _x = x; }
	void setY(const FastDec& y) { _y = y; }
	void setZ(const FastDec& z) { _z = z; }

	float length() const
	{
		return std::sqrt(_x * _x + _y * _y + _z * _z);
	};
    
    float dotProduct(const FastVec3& other) const
    {
        return float(_x * other._x + _y * other._y + _z * other._z);
    };

	void normalize();
	float angleToJUnit() const;

	std::string __repr__() const;

private:
	FastDec _x;
	FastDec _y;
	FastDec _z;

    explicit FastVec3(FastDec x, FastDec y, FastDec z): _x(x), _y(y), _z(z) { };
}; // class FastVec3

#endif // header guard
