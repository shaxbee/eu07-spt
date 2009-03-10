#ifndef SPTCORE_RAILTRACKING_H
#define SPTCORE_RAILTRACKING_H 1

#include <osg/Array>

namespace sptCore
{
    
class Path;

class RailTracking
{

public:
    virtual ~RailTracking() { };

    virtual RailTracking* getNext(RailTracking* tracking) = 0;
    virtual Path* getPath(RailTracking* tracking) = 0;
    virtual Path* reverse(Path* path) = 0;

}; // class sptCore::RailTracking

struct Path
{
    Path() { };
    Path(osg::Vec3Array* points, RailTracking* begin, RailTracking* end);
    
    Path* reverse();
    
    osg::ref_ptr<osg::Vec3Array> _points;
    RailTracking* _previous;
    RailTracking* _next;

    static Path* straight(osg::Vec3 begin, osg::Vec3 end, RailTracking* previous, RailTracking* next);
    static Path* bezier(osg::Vec3 begin, osg::Vec3 controlBegin, osg::Vec3 end, osg::Vec3 controlEnd, RailTracking* previous, RailTracking* next);
    
}; // class sptCore::Path

} // namespace sptCore

#endif // headerguard
