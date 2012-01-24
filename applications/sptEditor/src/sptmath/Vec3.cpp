#include "Vec3.h"

#define _USE_MATH_DEFINES // we need M_PI
#include <math.h>
#include <iostream>

#include <boost/format.hpp>

using namespace std;
using namespace boost;

Vec3 Vec3::normalized()
{
    double len = length();
    double x(_x);
    double y(_y);
    double z(_z);

    return Vec3(Decimal(x / len), Decimal(y / len), Decimal(z / len));
};

double Vec3::angleToJUnit() const
{
    double div = double(_y) / length();
    double theta = div <= -1.0 ? double(M_PI) : acos(div);

    if(double(_x) < -0.0)
        return 2 * double(M_PI) - theta;

    return theta;
};

std::string Vec3::__repr__() const
{
    return str(format("(%s,%s,%s)") % _x.__str__() % _y.__str__() % _z.__str__());
};

boost::int32_t Vec3::hash() const
{
    int seed = 17;

    seed = seed * 31 + _x.hash();
    seed = seed * 31 + _x.hash();
    seed = seed * 31 + _x.hash();

    return seed;
}
