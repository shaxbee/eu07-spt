#include <algorithm>

#include "sptCore/RailTracking.h"

using namespace sptCore;

Path* Path::reverse()
{
    
    Path* result = new Path;
    
    result->_begin = _end;
    result->_end = _begin;
    
    result->_points = new osg::Vec3Array(_points->size());
    
    std::reverse_copy(_points->begin(), _points->end(), result->_points->begin());
    
    return result;
    
}; // Path::reverse