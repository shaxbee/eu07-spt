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

    Path* path = new Path;
    path->reserve(2);

    path->push_back(begin);
    path->push_back(end);

    return std::make_pair(path, path->reverse());

}; // Path::straight

Path::Pair Path::bezier(osg::Vec3 begin, osg::Vec3 controlBegin, osg::Vec3 end, osg::Vec3 controlEnd, int steps)
{
    
    Path* path = new Path;
    
    float delta = (float) 1 / (float) steps - 1;
    path->reserve(steps);

    while(steps--)
    {

        float omt = steps * delta; // current t along path (range from 0 .. 1)
        float t = (1 - omt); // for faster computations we precalculate 1 - t

        // add point
        path->push_back(
            begin        * (omt * omt * omt) + 
            controlBegin * (3 * omt * omt * t) + 
            end          * (3 * omt * t * t) + 
            controlEnd   * (t * t * t)
        );

    };    
    
    return std::make_pair(path, path->reverse());

}; // Path::bezier
