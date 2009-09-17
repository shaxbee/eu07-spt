#include "sptCore/Path.h"

#include <algorithm>
#include <iterator>

using namespace sptCore;

Path* Path::reverse(const Path* source)
{
    
    Path* reversed = new Path;
    reversed->resize(source->size());

    std::reverse_copy(source->begin(), source->end(), reversed->begin());
    
    return reversed;
    
}; // static Path::reverse

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
