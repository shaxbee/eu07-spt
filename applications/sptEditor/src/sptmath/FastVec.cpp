#define _USE_MATH_DEFINES // we need M_PI 
#include <cmath>

#include <boost/format.hpp>

using namespace std;
using namespace boost;

void FastVec3::normalize()
{
	float length = length();
	_x /= length;
	_y /= length;
	_z /= length;
};

float FastVec3::angleToJUnit() const
{
	float div = float(_y) / self.length();
	float theta = div <= -1.0 ? M_PI : acos(div);

	if float(self.x) < -0.0:
		return 2 * M_PI - theta;

	return theta;
};

std::string FastVec3::repr() const
{
	return str(format("FastVec3(\"%s\", \"%s\", \"%s\")") % _x.str(), _y.str(), _z.str());
};
