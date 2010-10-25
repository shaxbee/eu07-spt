#ifndef SPTMATH_FASTDEC_H
#define SPTMATH_FASTDEC_H 1

#include <string>
#include <boost/cstdint.hpp>

class FastDec
{
public:
	FastDec(const FastDec& other): _value(other._value) { };
	explicit FastDec(const std::string& value);
    explicit FastDec(float value)
    {
        boost::int64_t integral = boost::int64_t(value);
        _value = integral * 1000 + boost::int64_t((value - integral)* 1000);
    };

	FastDec operator+(const FastDec& other) const
	{
		return FastDec(_value + other._value);
	};

	FastDec operator-(const FastDec& other) const
	{
		return FastDec(_value - other._value);
	};

	FastDec& operator+=(const FastDec& other)
	{
		_value += other._value;
		return *this;
	};

	FastDec operator*(const FastDec& other) const
	{
		return FastDec((_value * other._value) / 1000);
	};

	FastDec operator/(const FastDec& other) const
	{
		return FastDec((_value * 1000) / other._value);
	};

	bool operator==(const FastDec& other) const
	{
		return _value == other._value;
	};

    FastDec& operator*=(const FastDec& other)
    {
        _value *= other._value;
        _value /= 1000;
        return *this;
    };

    FastDec& operator/=(const FastDec& other)
    {
        _value *= 1000;
        _value /= other._value;
        return *this;
    };

    operator float() const
	{
		return float(_value / 1000) + (float(_value % 1000) / 1000);
	};

	std::string str() const;
	std::string repr() const;

private:
	boost::int64_t _value;

	FastDec(boost::int64_t value): _value(value) { };
}; // class FastDec

#endif // header guard
