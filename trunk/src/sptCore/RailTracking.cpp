#include <algorithm>

#include "sptCore/RailTracking.h"

using namespace sptCore;

Path* Path::reverse() const
{
    
    Path* reversed = new Path(size());
    std::reverse_copy(begin(), end(), reversed->begin());
    
    return reversed;
    
}; // Path::reverse

Path::Pair Path::straight(osg::Vec3 begin, osg::Vec3 end)
{

    Path* path = new Path(2);

    path->push_back(begin);
    path->push_back(end);

    return std::make_pair(path, path->reverse());

}; // Path::straight

Path::Pair Path::bezier(osg::Vec3 begin, osg::Vec3 controlBegin, osg::Vec3 end, osg::Vec3 controlEnd)
{

    return Path::straight(begin, end);

}; // Path::bezier
