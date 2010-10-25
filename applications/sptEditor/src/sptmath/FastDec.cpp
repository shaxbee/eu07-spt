#include "FastDec.h"

#include <stdexcept>

#include <boost/format.hpp>
#include <boost/lexical_cast.hpp>

using namespace std;
using namespace boost;

FastDec::FastDec(const string& value)
{
	size_t separator = value.find('.');

	try
	{
		// convert decimal part
		uint64_t decimal = lexical_cast<uint64_t>(value.substr(0, separator));

		// extract fractional part if present
		string fractionalStr = separator != string::npos ? value.substr(separator + 1) : "0";

		// count number of zeros for proper base multiplication
		size_t zeros = fractionalStr.find_first_not_of('0'); 
		uint64_t fractional = lexical_cast<uint64_t>(fractionalStr) * uint64_t(pow(float(10), int(zeros != string::npos ? zeros + 1 : 0)));

		_value = decimal * 1000 + fractional;
	}
	catch(bad_lexical_cast&)
	{
        throw runtime_error(boost::str(format("FastDec::FastDec(value): Value \"%s\" cannot be converted to decimal number") % value));
	};
};

std::string FastDec::str() const
{
    return boost::str(format("%d.%04d") % (_value / 1000) % (_value % 1000));
};

std::string FastDec::repr() const
{
    return boost::str(format("FastDec(\"%d.%04d\")") % (_value / 1000) % (_value % 1000));
};
