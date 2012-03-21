#include "sptCore/Path.h"

#include <algorithm>
#include <iterator>

#include <boost/assert.hpp>

using namespace sptCore;

namespace
{

static const unsigned int BEZIER_RECURSION_LIMIT = 9;
static const double BEZIER_TOLERANCE_BASE = 0.18;

double pointDistance(const osg::Vec3f& from, const osg::Vec3f& to, const osg::Vec3f& point)
{

    osg::Vec3f v = to - from;
    osg::Vec3f w = point - from;

    double c1 = w * v;
    if(c1 <= 0)
        return (point - from).length();

    double c2 = v * v;
    if(c2 <= c1)
        return (point - to).length();

    return (point - (from + v * (c1 / c2))).length();

};

void recursiveBezier(osg::Vec3Array& dest, const osg::Vec3& p1, const osg::Vec3& p2, const osg::Vec3& p3, const osg::Vec3& p4, const float& tolerance, unsigned depth)
{

    osg::Vec3f p12 = (p1 + p2) / 2;
    osg::Vec3f p23 = (p2 + p3) / 2;
    osg::Vec3f p34 = (p3 + p4) / 2;
    osg::Vec3f p123 = (p12 + p23) / 2;
    osg::Vec3f p234 = (p23 + p34) / 2;
    osg::Vec3f p1234 = (p123 + p234) / 2;

    osg::Vec3f delta = p4 - p1;

    double dist = (pointDistance(p1, p4, p2) + pointDistance(p1, p4, p3)) / 2;

    if(dist < tolerance * delta.length())
    {
        dest.push_back(p1234);
    }
    else if(depth < BEZIER_RECURSION_LIMIT)
    {
        recursiveBezier(dest, p1, p12, p123, p1234, tolerance, depth + 1);
        recursiveBezier(dest, p1234, p234, p34, p4, tolerance, depth + 1);
    };

};

osg::ref_ptr<osg::Vec3Array> createPoints(osg::Vec3 p1, osg::Vec3 cp1, osg::Vec3 p2, osg::Vec3 cp2, float scale)
{

    double tolerance = BEZIER_TOLERANCE_BASE / scale;
    tolerance *= tolerance;

    osg::ref_ptr<osg::Vec3Array> result(new osg::Vec3Array);
    result->push_back(p1);
    recursiveBezier(*result, p1, cp1, cp2, p2, tolerance, 1);
    result->push_back(p2);

    return result;

};

class CurveLength
{
public:
    CurveLength(const osg::Vec3& first): _previous(first), _length(0.0f) { };

    void operator()(const osg::Vec3& current)
    {
        _length += (current - _previous).length();
    };

    float result() const { return _length; }

private:
    osg::Vec3 _previous;
    float _length;
};

float calcLength(const osg::Vec3Array& points)
{
    BOOST_ASSERT(points.size() >= 2);

    float result(0.0f);
    osg::Vec3f previous(points.front());

    for(osg::Vec3Array::const_iterator iter = points.begin() + 1; iter != points.end(); previous = *iter, iter++)
    {
        result += (*iter - previous).length();
    };

    return result;
};

}; // anonymous namespace

StraightPath::~StraightPath()
{
};

std::auto_ptr<Path> StraightPath::clone() const
{
    return std::auto_ptr<Path>(new StraightPath(front(), back()));
};

std::auto_ptr<Path> StraightPath::reverse() const
{
    return std::auto_ptr<Path>(new StraightPath(back(), front()));
};

float StraightPath::length() const
{
    return (front() - back()).length();
};

osg::Vec3f StraightPath::frontDir() const
{
    osg::Vec3f result(back() - front());
    result.normalize();
    return result;
};

osg::Vec3f StraightPath::backDir() const
{
    return frontDir();
};

osg::ref_ptr<osg::Vec3Array> StraightPath::points(float scale) const
{
    osg::Vec3Array* result = new osg::Vec3Array;
    result->push_back(front());
    result->push_back(back());
    return result;
};

BezierPath::BezierPath(const osg::Vec3f& front, const osg::Vec3f& frontCP, const osg::Vec3f& back, const osg::Vec3f& backCP):
    Path(front, back), _frontCP(frontCP), _backCP(backCP)
{
    _points = createPoints(front, frontCP, back, backCP, DEFAULT_SCALE);
    _length = calcLength(*_points);
};

BezierPath::BezierPath(const osg::Vec3f& front, const osg::Vec3f& frontCP, const osg::Vec3f& back, const osg::Vec3f& backCP, const float length):
    Path(front, back), _frontCP(frontCP), _backCP(backCP), _length(length)
{
    _points = createPoints(front, frontCP, back, backCP, DEFAULT_SCALE);
};

BezierPath::~BezierPath()
{
};

osg::Vec3f BezierPath::frontDir() const
{
    osg::Vec3f result(_frontCP - front());
    result.normalize();

    return result;
};

osg::Vec3f BezierPath::backDir() const
{
    osg::Vec3f result(-_backCP + back());
    result.normalize();

    return result;
};

std::auto_ptr<Path> BezierPath::clone() const
{
    return std::auto_ptr<Path>(new BezierPath(front(), _frontCP, back(), _backCP));
};

std::auto_ptr<Path> BezierPath::reverse() const
{
    std::auto_ptr<BezierPath> result(new BezierPath(back(), _backCP, front(), _frontCP, _length));

    // if source path was initialized
    if(_points.valid())
    {
        // reverse copy points
        osg::ref_ptr<osg::Vec3Array> reversed(new osg::Vec3Array(points()->rbegin(), points()->rend()));
        result->_points = reversed;
    };

    return std::auto_ptr<Path>(result);
};

float BezierPath::length() const
{
    return _length;
};

osg::ref_ptr<osg::Vec3Array> BezierPath::points(float scale) const
{
    if(scale == DEFAULT_SCALE && _points.valid())
    {
        return _points;
    };

    return createPoints(front(), frontCP(), back(), backCP(), scale);
};

const float sptCore::Path::DEFAULT_SCALE = 1.4f;
