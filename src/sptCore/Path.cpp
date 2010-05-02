#include "sptCore/Path.h"

#include <algorithm>
#include <iterator>

#include <boost/math/special_functions/fpclassify.hpp>

using namespace sptCore;

namespace
{

osg::ref_ptr<osg::Vec3Array> createPoints(float scale)
{

};

class CalculateLength
{

public:
    CalculateLength(): _length(std::numeric_limits<float>::quiet_NaN()) { };

    void operator()(const osg::Vec3f& point)
    {

        if(boost::math::isnan(_length))
            _length = 0;
        else
            _length += (point - _last).length();

        _last = point;

    };

    float length() { return _length; }

private:
    float _length;
    osg::Vec3f _last;

}; // class <anonymous>::CalculateLength

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
    osg::Vec3f result(-(front() - back()));
    result.normalize();
    return result;
};

osg::Vec3f StraightPath::backDir() const
{
    osg::Vec3f result(-(back() - front()));
    result.normalize();
    return result;
};

osg::ref_ptr<osg::Vec3Array> StraightPath::points(float scale) const 
{
    osg::Vec3Array* result = new osg::Vec3Array;
    result->push_back(front());
    result->push_back(back());
    return result;
};

std::auto_ptr<Path> BezierPath::reverse() const
{
    std::auto_ptr<BezierPath> result(new BezierPath(back(), _backCP, front(), _frontCP));

    // if source path was initialized
    if(!boost::math::isnan(_length))
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
    if(boost::math::isnan(_length))
    {
        CalculateLength calc;
        osg::ref_ptr<osg::Vec3Array> pts(points());

        std::for_each(pts->begin(), pts->end(), calc);

        _length = calc.length();
    };

    return _length;
};

osg::ref_ptr<osg::Vec3Array> BezierPath::points(float scale) const
{
    Entries::iterator iter = std::find_if(_entries.begin(), _entries.end(), FindBezierPathEntry(scale));

    osg::ref_ptr<osg::Vec3Array> result;

    if(iter == _entries.end())
    {
        result = createPoints(scale);
        _entries.push_back(std::make_pair(scale, result));
    }
    else
    {
        result = iter->second;
    };

    return result;
};

# if 0
Path* Path::reverse() const
{
    
    Path* reversed = new Path;
    reversed->resize(size());

    std::reverse_copy(begin(), end(), reversed->begin());
    
    return reversed;
    
}; // Path::reverse



Path::Path(osg::Vec3 front, osg::Vec3 back):
    _frontDir(back - front), _backDir(_frontDir), _length(_frontDir.length()), _frontRoll(0), _backRoll(0)
{

    _frontDir.normalize();
    _backDir.normalize();

    reserve(2);

    push_back(front);
    push_back(back);

}; // Path::Path(front, back)

Path::Path(osg::Vec3 front, osg::Vec3 frontCP, osg::Vec3 back, osg::Vec3 backCP, int steps, float frontRoll, float backRoll):
    _frontDir(frontCP - front), _backDir(-backCP + back), _length(0), _frontRoll(frontRoll), _backRoll(backRoll)
{

    _frontDir.normalize();
    _backDir.normalize();

    float delta = (float) 1 / (float) steps;
    reserve(steps);

    osg::Vec3 previous(front);

    for(unsigned int i = 0; i <= steps; i++)
    {

        float t = i * delta; // current t along path (range from 0 .. 1)
        float omt = 1 - t; 

        // add point
        push_back(
            front   * (omt * omt * omt) + 
            frontCP * (3 * omt * omt * t) + 
            backCP  * (3 * omt * t * t) + 
            back    * (t * t * t)
        );

        const osg::Vec3 delta = this->back() - previous;
        _length += delta.length();
        previous = this->back();

    };
    
}; // Path::Path(front, frontCP, back, backCP, steps)

#endif
