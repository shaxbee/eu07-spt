#ifndef SPTCORE_RAILTRACKING_H
#define SPTCORE_RAILTRACKING_H 1

#include <vector>

#include <osg/Vec3>
#include <osg/Node>

namespace sptCore
{

class RailTracking: public osg::Node
{

public:
    typedef std::vector<osg::Vec3f> Path;

    virtual RailTracking* getNext(RailTracking* tracking) = 0;
    virtual Path* getPath(RailTracking* tracking) = 0;

}; // class sptCore::RailTracking

} // namespace sptCore

#endif // headerguard
