#include <algorithm>

#include "sptCore/RailTracking.h"

using namespace sptCore;

Path::Path(osg::Vec3Array* points, RailTracking* previous, RailTracking* next):
    _points(points), _previous(previous), _next(next)
{

}; // Path::Path

Path* Path::reverse()
{
    
    osg::Vec3Array* reversed = new osg::Vec3Array(_points->size());
    std::reverse_copy(_points->begin(), _points->end(), reversed->begin());
    
    return new Path(reversed, _next, _previous);
    
}; // Path::reverse

Path* Path::straight(osg::Vec3 begin, osg::Vec3 end, RailTracking* previous, RailTracking* next)
{

    osg::Vec3Array* points = new osg::Vec3Array(2);
    points->push_back(begin);
    points->push_back(end);

    return new Path(points, previous, next);

}; // Path::straight

Path* Path::bezier(osg::Vec3 begin, osg::Vec3 controlBegin, osg::Vec3 end, osg::Vec3 controlEnd, RailTracking* previous, RailTracking* next)
{

    return new Path();

}; // Path::bezier
