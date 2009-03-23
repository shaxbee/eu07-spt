#ifndef SPTCORE_RAILTRACKING_H
#define SPTCORE_RAILTRACKING_H 1

#include <boost/exception.hpp> 
#include <osg/Vec3>

namespace sptCore
{
    
class Path;

class RailTracking
{

public:
    virtual ~RailTracking() { };

    virtual osg::Vec3 getExit(osg::Vec3 entry) const = 0;
    virtual Path* getPath(osg::Vec3 entry) const = 0;
    virtual Path* reverse(Path* path) const = 0;

    typedef boost::error_info<struct tag_position, osg::Vec3f> PositionInfo;
    typedef boost::error_info<struct tag_path, Path*> PathInfo;

    class UnknownEntryException: public boost::exception { };
    class UnknownPathException: public boost::exception { };

}; // class sptCore::RailTracking

} // namespace sptCore

#endif // headerguard
