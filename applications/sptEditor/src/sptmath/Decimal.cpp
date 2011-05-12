#include "Decimal.h"

#include <iostream>
#include <stdexcept>
#include <cmath>
#include <sstream>

#include <boost/format.hpp>
#include <boost/lexical_cast.hpp>

using namespace std;
using namespace boost;

Decimal::Decimal(const string& value, uint8_t precision)
{
	size_t separator = value.find('.');

	try
	{
        _base = pow(10, precision);
		int64_t decimal = abs(lexical_cast<int64_t>(value.substr(0, separator)));

		// extract fractional part if present
        if(separator != string::npos)
        {
		    string fract_str = value.substr(separator + 1);
            float fractional = lexical_cast<float>(fract_str) * pow(10, int(-fract_str.size() + precision));
            _value = decimal * _base + int64_t(floor(fractional+0.5));
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
