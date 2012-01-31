#include "Decimal.h"

#include <iostream>
#include <stdexcept>
#include <cmath>
#include <sstream>

#include <boost/format.hpp>
#include <boost/lexical_cast.hpp>

#include <boost/math/special_functions/sign.hpp>
#include <boost/math/special_functions/round.hpp>

using namespace std;
using namespace boost;
using namespace boost::math;

namespace
{
	uint32_t pow10(uint8_t exp)
	{
		return uint32_t(pow(double(10), exp));
	};
};

Decimal::Decimal():
	_value(0), 
	_base(pow10(DEFAULT_PRECISION)) 
{ 
};

Decimal::Decimal(const string& value, uint8_t precision):
	_base(pow10(precision))
{
    size_t separator = value.find('.');

    try
    {
        int64_t decimal = abs(long(lexical_cast<int64_t>(value.substr(0, separator))));

        // extract fractional part if present
        if(separator != string::npos)
        {
            string fract_str = value.substr(separator + 1);
            double fractional = lexical_cast<float>(fract_str) * pow(float(10.0), int32_t(precision - fract_str.size()));
            _value = decimal * _base + int64_t(floor(fractional + 0.5));
        }
        else
        {
            _value = decimal * _base;
        };

        if(value[0] == '-' && _value > 0)
            _value = -_value;
    }
    catch(bad_lexical_cast&)
    {
        throw runtime_error(str(format("Decimal::Decimal(value): Value \"%s\" cannot be converted to decimal number") % value));
    };
};

Decimal::Decimal(double value, boost::uint8_t precision):
	_base(pow10(precision))
{
    int64_t integral = int64_t(value);
	
	double tweaker = 0.005; // tweaker use to overcome floating number approximation issues
	double fractional = (value - integral) * _base;

	_value = 
		integral * _base + // integral part
		iround(abs(fractional) + tweaker) * sign(value); // fractional part, rounded symmetrically
};

Decimal Decimal::operator*(double other) const
{
	double integral = double(_value / _base) * other;
	double remainder = integral - floor(integral);
	integral -= remainder;

	double fractional = double((_value % _base)) * other + remainder * _base;
	const double tweaker = 0.005; // tweaker use to overcome floating number approximation issues

	int64_t value = 
		int64_t(integral) * _base + // integral part
		iround(abs(fractional) + tweaker) * sign(fractional);

	return Decimal(value, _base);
};

std::string Decimal::__repr__() const
{
    return str(format("Decimal(\'%s\')") % __str__());
};

std::string Decimal::__str__() const
{
    int64_t fractional = _value % _base;
    int64_t decimal = (_value - fractional) / _base;

    ostringstream result;

    if(decimal >= 0 && fractional < 0)
    {
        result << '-';
    };

    result << decimal << ".";

    string fraction_str = boost::lexical_cast<string>(abs(int(fractional)));
    uint8_t prec = precision();

    if(fraction_str.size() < prec)
    {
        result << std::string(size_t(prec) - fraction_str.size(), '0');
    };

    result << fraction_str;

    return result.str();
};

