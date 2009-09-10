#ifndef SPTCORE_SWITCH_H
#define SPTCORE_SWITCH_H 1

#include <sptCore/SwitchableTracking.h>

namespace sptCore
{

class Switch: public SwitchableTracking
{

public:
    //! Construct switch described by bezier path
    //! \param p1 common point
    //! \param cp1 common control vector
    //! \param p2 end of straight path
    //! \param cp2 straight path control vector
    //! \param p3 end of diverted path
    //! \param cp3 diverted path control vector
    //! \param position initial position
    Switch(const osg::Vec3& p1, const osg::Vec3& cp1, const osg::Vec3& p2, const osg::Vec3& cp2, const osg::Vec3& p3, const osg::Vec3& cp3, const std::string& position = "STRAIGHT"); 
    virtual ~Switch() { };

    virtual osg::Vec3 getExit(const osg::Vec3& entry) const;
    virtual Path* getPath(const osg::Vec3& entry) const;

    virtual void setPosition(const std::string& position);
    virtual const ValidPositions getValidPositions() const { return _positions; }

    Path* getStraightPath() const { return _straight.first.get(); }
    Path* getDivertedPath() const { return _diverted.first.get(); }

protected:
    static Positions _positions;

    typedef std::pair<boost::shared_ptr<Path>, boost::shared_ptr<Path> > PathPair;

    PathPair _straight;
    PathPair _diverted;

}; // class Switch

} // namespace sptCore

#endif // headerguard
