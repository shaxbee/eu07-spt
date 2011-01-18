#include "Decimal.h"

#include <iostream>
#include <stdexcept>
#include <cmath>

#include <boost/format.hpp>
#include <boost/lexical_cast.hpp>

using namespace std;
using namespace boost;

Decimal::Decimal(const string& value)
{
	size_t separator = value.find('.');

	try
	{
		// convert decimal part
		int64_t decimal = lexical_cast<int64_t>(value.substr(0, separator));

		// extract fractional part if present
		string fractionalStr = separator != string::npos ? value.substr(separator + 1) : "0";
        float fractional = lexical_cast<float>(fractionalStr) * pow(10.0f, -int(fractionalStr.size()) + 3);

        _value = decimal * 1000 + int64_t(floor(fractional+0.5));

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
    return str(format("Decimal(\"%s\")") % __str__());
};

std::string Decimal::__str__() const
{
    int64_t fractional = _value % 1000;
    int64_t decimal = (_value - fractional) / 1000;

    return str(format("%s%d.%03d") % (decimal >= 0 && fractional < 0 ? "-" : "") % decimal % abs(int(fractional)));
};
