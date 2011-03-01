#ifndef SPTMATH_DECIMAL_H
#define SPTMATH_DECIMAL_H 1

#include <string>
#include <boost/cstdint.hpp>

class Decimal
{
public:
    Decimal(): _value(0) { };
	Decimal(const Decimal& other): _value(other._value) { };
	explicit Decimal(const std::string& value);
    explicit Decimal(float value)
    {
        boost::int64_t integral = boost::int64_t(value);
        _value = integral * 1000 + boost::int64_t((value - integral) * 1000);
    };

	Decimal operator+(const Decimal& other) const
	{
		return Decimal(_value + other._value);
	};

	Decimal operator-(const Decimal& other) const
	{
		return Decimal(_value - other._value);
	};

    Decimal operator-() const
    {
        return Decimal(-_value);
    };

	Decimal& operator+=(const Decimal& other)
	{
		_value += other._value;
		return *this;
	};

	Decimal operator*(const Decimal& other) const
	{
		return Decimal((_value * other._value) / 1000);
	};

	Decimal operator/(const Decimal& other) const
	{
		return Decimal((_value * 1000) / other._value);
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
        _value /= 1000;
        return *this;
    };

    Decimal& operator/=(const Decimal& other)
    {
        _value *= 1000;
        _value /= other._value;
        return *this;
    };

    operator float() const
	{
		return float(_value / 1000) + (float(_value % 1000) / 1000);
	};

    boost::int64_t raw() const { return _value; }

	std::string __repr__() const;
    std::string __str__() const;

private:
	boost::int64_t _value;

	Decimal(boost::int64_t value): _value(value) { };
}; // class Decimal

#endif // header guard
