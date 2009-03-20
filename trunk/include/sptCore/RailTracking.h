#ifndef SPTCORE_RAILTRACKING_H
#define SPTCORE_RAILTRACKING_H 1

#include <boost/exception.hpp> 
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

    typedef boost::error_info<struct tag_position, osg::Vec3f> PositionInfo;
    typedef boost::error_info<struct tag_path, Path*> PathInfo;

    class UnknownEntryException: public boost::exception { };
    class UnknownPathException: public boost::exception { };

}; // class sptCore::RailTracking

class Path: public osg::Vec3Array
{

public:
    Path(): osg::Vec3Array() { }
    Path(size_t size): osg::Vec3Array(size) { }

    typedef std::pair<osg::ref_ptr<Path>, osg::ref_ptr<Path> > Pair;
    
    static Pair straight(osg::Vec3 begin, osg::Vec3 end);
    static Pair bezier(osg::Vec3 begin, osg::Vec3 cpBegin, osg::Vec3 end, osg::Vec3 cpEnd, int steps);

private:
    Path* reverse() const;

}; // class sptCore::Path

} // namespace sptCore

#endif // headerguard
