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

    virtual osg::Vec3 getExit(osg::Vec3 entry) = 0;
    virtual Path* getPath(osg::Vec3 entry) = 0;
    virtual Path* reverse(Path* path) = 0;

}; // class sptCore::RailTracking

class Path: public osg::Vec3Array
{

public:
    Path(size_t size): osg::Vec3Array(size) { }

    typedef std::pair<osg::ref_ptr<Path>, osg::ref_ptr<Path> > Pair;
    
    static Pair straight(osg::Vec3 begin, osg::Vec3 end);
    static Pair bezier(osg::Vec3 begin, osg::Vec3 cpBegin, osg::Vec3 end, osg::Vec3 cpEnd);

private:
    Path* reverse() const;

}; // class sptCore::Path

} // namespace sptCore

#endif // headerguard
