#ifndef SPTMATH_DECIMAL_H
#define SPTMATH_DECIMAL_H 1

#include <string>
#include <cmath>
#include <boost/cstdint.hpp>

class Decimal
{
public:
    static const uint8_t DEFAULT_PRECISION = 3;

    Decimal(): _value(0), _base(std::pow(10, DEFAULT_PRECISION)) { };
	Decimal(const Decimal& other): _value(other._value), _base(other._base) { };
	explicit Decimal(const std::string& value, boost::uint8_t precision = DEFAULT_PRECISION);
    explicit Decimal(float value, boost::uint8_t precision = DEFAULT_PRECISION)
    {
        _base = std::pow(10, precision);
        boost::int64_t integral = boost::int64_t(value);
        _value = integral * _base + boost::int64_t((value - integral) * _base);
    };

	Decimal operator+(const Decimal& other) const
	{
		return Decimal(_value + other._value, _base);
	};

	Decimal operator-(const Decimal& other) const
	{
		return Decimal(_value - other._value, _base);
	};

    Decimal operator-() const
    {
        return Decimal(-_value, _base);
    };

	Decimal& operator+=(const Decimal& other)
	{
		_value += other._value;
		return *this;
	};

	Decimal operator*(const Decimal& other) const
	{
		return Decimal((_value * other._value) / _base, _base);
	};

	Decimal operator/(const Decimal& other) const
	{
		return Decimal((_value * _base) / other._value, _base);
	};

	bool operator==(const Decimal& other) const
	{
		return _value == other._value;
	};

    operator bool() const
    {
        return _value != 0;
    };

    Decimal& operator*=(const Decimal& other)
    {
        _value *= other._value;
        _value /= _base;
        return *this;
    };

    Decimal& operator/=(const Decimal& other)
    {
        _value *= _base;
        _value /= other._value;
        return *this;
    };

    operator float() const
	{
		return float(_value / _base) + (float(_value % _base) / _base);
	};

    boost::uint8_t precision() const { return std::log10(float(_base)); }
    boost::uint32_t base() const { return _base; }
    boost::int64_t raw() const { return _value; }

	std::string __repr__() const;
    std::string __str__() const;

private:
	boost::int64_t _value;
    boost::uint32_t _base;

	Decimal(boost::int64_t value, boost::int32_t base): _value(value), _base(base) { };
}; // class Decimal

#endif // header guard
