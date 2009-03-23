#ifndef SPTCORE_SWITCH_H
#define SPTCORE_SWITCH_H 1

#include "sptCore/RailTracking.h"
#include "sptCore/Path.h"

namespace sptCore
{

class Switch: public RailTracking
{

public:
    Switch(osg::Vec3 p1, osg::Vec3 cp1, osg::Vec3 p2, osg::Vec3 cp2, osg::Vec3 p3, osg::Vec3 cp3); 
    virtual ~Switch() { };

    virtual osg::Vec3 getExit(osg::Vec3 entry) const;
    virtual Path* getPath(osg::Vec3 entry) const;
    virtual Path* reverse(Path* path) const;

    typedef enum { STRAIGHT, DIVERTED } Position;

    Position getPosition() const { return _position; }
    void setPosition(Position position) { _position = position; }

protected:
    Position _position;

    Path::Pair _straight;
    Path::Pair _diverted;

}; // class Switch

} // namespace sptCore

#endif // headerguard
