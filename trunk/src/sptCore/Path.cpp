#include "sptCore/Path.h"

#include <algorithm>
#include <iterator>

using namespace sptCore;

Path* Path::reverse() const
{
    
    Path* reversed = new Path;
    reversed->resize(size());

    std::reverse_copy(begin(), end(), reversed->begin());
    
    return reversed;
    
}; // Path::reverse

Path::Path(osg::Vec3 front, osg::Vec3 back):
    _frontCP(back - front), _backCP(front - back)
{

    reserve(2);

    push_back(front);
    push_back(back);

}; // Path::Path(front, back)

Path::Path(osg::Vec3 front, osg::Vec3 frontCP, osg::Vec3 back, osg::Vec3 backCP, int steps, float frontRoll, float backRoll):
    _frontCP(frontCP), _backCP(backCP), _frontRoll(frontRoll), _backRoll(backRoll)
{
    
    float delta = (float) 1 / (float) steps;
    reserve(steps);

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

    };    
    
}; // Path::Path(front, frontCP, back, backCP, steps)

Path::Pair Path::straight(osg::Vec3 front, osg::Vec3 back)
{

    osg::ref_ptr<Path> path = new Path(front, back);
    return Pair(path, osg::ref_ptr<Path>(path->reverse()));

}; // Path::straight

Path::Pair Path::bezier(osg::Vec3 front, osg::Vec3 frontCP, osg::Vec3 back, osg::Vec3 backCP, int steps)
{

    osg::ref_ptr<Path> path = new Path(front, frontCP, back, backCP, steps);
    return Pair(path, osg::ref_ptr<Path>(path->reverse()));

}; // Path::bezier
