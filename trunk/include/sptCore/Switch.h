#ifndef SPTCORE_SWITCH_H
#define SPTCORE_SWITCH_H 1

#include "sptCore/RailTracking.h"
#include "sptCore/Path.h"

namespace sptCore
{

class Switch: public RailTracking
{

public:
    typedef enum { STRAIGHT, DIVERTED } Position;

    //! Construct switch described by bezier path
    //! \param p1 common point
    //! \param cp1 common control vector
    //! \param p2 end of straight path
    //! \param cp2 straight path control vector
    //! \param p3 end of diverted path
    //! \param cp3 diverted path control vector
    //! \param position initial position
    Switch(osg::Vec3 p1, osg::Vec3 cp1, osg::Vec3 p2, osg::Vec3 cp2, osg::Vec3 p3, osg::Vec3 cp3, Position position = STRAIGHT); 
    virtual ~Switch() { };

    virtual osg::Vec3 getExit(const osg::Vec3& entry) const;
    virtual Path* getPath(const osg::Vec3& entry) const;

//    virtual void enter(Follower* follower, const osg::Vec3& entry) { };
//    virtual void leave(Follower* follower, const osg::Vec3& entry) { };

    Position getPosition() const { return _position; }
    void setPosition(Position position) { _position = position; }

    Path* getStraightPath() const { return _straight.first; }
    Path* getDivertedPath() const { return _diverted.first; }

protected:
    Position _position;

    typedef std::pair<Path*, Path*> PathPair;

    PathPair _straight;
    PathPair _diverted;

}; // class Switch

} // namespace sptCore

#endif // headerguard
