#include "sptCore/Path.h"

#include <algorithm>
#include <iterator>

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
    recursiveBezier(*result, p1, cp1, cp2, p2, tolerance, 1);
    return result;

};


struct FindBezierPathEntry
{

    FindBezierPathEntry(float resolution): _resolution(resolution) { };

    template <typename PairT>
    bool operator()(const PairT& entry)
    {

        return entry.first == _resolution;

    };

    float _resolution;

}; // class <anonymous>::FindBezierPathEntry

}; // anonymous namespace

const float Path::DEFAULT_SCALE;

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

osg::Vec3f BezierPath::frontDir() const
{
    osg::Vec3f result(_frontCP);
    result.normalize();

    return result;
};

osg::Vec3f BezierPath::backDir() const
{
    osg::Vec3f result(-_backCP);
    result.normalize();

    return result;
};

std::auto_ptr<Path> BezierPath::reverse() const
{
    std::auto_ptr<BezierPath> result(new BezierPath(back(), _backCP, front(), _frontCP));

    // if source path was initialized
    if(_length)
    {
        // initialize length to avoid overhead
        result->_length = _length;

        // reverse copy points
        osg::ref_ptr<osg::Vec3Array> reversedPoints(new osg::Vec3Array(points()->rbegin(), points()->rend()));
        result->_entries.push_back(Entry(DEFAULT_SCALE, reversedPoints));
    };

    return std::auto_ptr<Path>(result);
};

float BezierPath::length() const
{

    // lazy initialization
    if(!_length)
    {
        double length = 0.0f;

        const osg::Vec3Array& pts = *(points());
        for(osg::Vec3Array::const_iterator iter = pts.begin(); iter != pts.end() - 1; iter++)
            length += (*(iter + 1) - *iter).length();
        
        _length = length;
    };

    return _length;
};

osg::ref_ptr<osg::Vec3Array> BezierPath::points(float scale) const
{
    Entries::iterator iter = std::find_if(_entries.begin(), _entries.end(), FindBezierPathEntry(scale));

    osg::ref_ptr<osg::Vec3Array> result;

    if(iter == _entries.end())
    {
        result = createPoints(front(), _frontCP, back(), _backCP, scale);
        _entries.push_back(std::make_pair(scale, result));
    }
    else
    {
        result = iter->second;
    };

    return result;
};

