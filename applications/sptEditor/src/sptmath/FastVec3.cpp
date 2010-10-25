#include "FastVec3.h"

#define _USE_MATH_DEFINES // we need M_PI 
#include <math.h>

#include <boost/format.hpp>

using namespace std;
using namespace boost;

void FastVec3::normalize()
{
	float len = length();
	_x /= FastDec(len);
	_y /= FastDec(len);
	_z /= FastDec(len);
};

float FastVec3::angleToJUnit() const
{
	float div = float(_y) / length();
	float theta = div <= -1.0 ? float(M_PI) : acos(div);

	if(float(_x) < -0.0)
		return 2 * float(M_PI) - theta;

	return theta;
};

std::string FastVec3::repr() const
{
	return str(format("FastVec3(\"%s\", \"%s\", \"%s\")") % _x.str() % _y.str() % _z.str());
};
