#ifndef SPTCORE_RAILTRACKING_H
#define SPTCORE_RAILTRACKING_H 1

#include <osg/Array>

namespace sptCore
{
    
class Path;

class RailTracking
{

public:
    virtual RailTracking* getNext(RailTracking* tracking) = 0;
    virtual Path* getPath(RailTracking* tracking) = 0;
    virtual Path* reverse(Path* path) = 0;

}; // class sptCore::RailTracking

struct Path
{
    
    Path* reverse();
    
    RailTracking* _begin;
    RailTracking* _end;
    osg::ref_ptr<osg::Vec3Array> _points;
    
}; // class sptCore::Path

} // namespace sptCore

#endif // headerguard
