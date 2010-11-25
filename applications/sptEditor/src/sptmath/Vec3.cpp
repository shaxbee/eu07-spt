#include "Vec3.h"

#define _USE_MATH_DEFINES // we need M_PI 
#include <math.h>

#include <boost/format.hpp>

using namespace std;
using namespace boost;

void Vec3::normalize()
{
	float len = length();
	_x /= Decimal(len);
	_y /= Decimal(len);
	_z /= Decimal(len);
};

float Vec3::angleToJUnit() const
{
	float div = float(_y) / length();
	float theta = div <= -1.0 ? float(M_PI) : acos(div);

	if(float(_x) < -0.0)
		return 2 * float(M_PI) - theta;

	return theta;
};

std::string Vec3::__repr__() const
{
    return str(format("(%s,%s,%s)") % _x.__str__() % _y.__str__() % _z.__str__());
};
