#ifndef SPTMATH_DECIMAL_H
#define SPTMATH_DECIMAL_H 1

#include <string>
#include <cmath>
#include <boost/cstdint.hpp>
#include <boost/functional/hash.hpp>

class Decimal
{
public:
    static const boost::uint8_t DEFAULT_PRECISION = 3;

    Decimal();
    Decimal(const Decimal& other): _value(other._value), _base(other._base) { };
    explicit Decimal(const std::string& value, boost::uint8_t precision = DEFAULT_PRECISION);
    explicit Decimal(double value, boost::uint8_t precision = DEFAULT_PRECISION);

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
        boost::int64_t temp = _value * other._value;
        if(temp < _base && temp >= (_base / 2))
            temp = _base;
        return Decimal(temp / _base, _base);
    };

	Decimal operator*(double other) const;

    Decimal operator/(const Decimal& other) const
    {
        return Decimal((_value * _base) / other._value, _base);
    };

    bool operator==(const Decimal& other) const
    {
        return _value == other._value;
    };

    boost::int32_t compareTo(const Decimal& other) const
    {
		boost::int64_t diff = _value - other._value;
        return diff < 0 ? -1 : (diff > 0 ? 1 : 0);
    }

    boost::int32_t hash() const
    {
        return boost::hash_value(_value);
    }

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

    operator double() const
    {
        return double(_value / _base) + (double(_value % _base) / _base);
    };

    boost::int64_t to_floor() const { return (_value / _base) - ((_value < 0 && (_value % _base != 0)) ? 1 : 0); }
    boost::int64_t to_ceiling() const { return (_value / _base) + ((_value % _base != 0) && (_value > 0) ? 1 : 0); }

	boost::uint8_t precision() const { return boost::uint8_t(std::log10(float(_base))); }
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
