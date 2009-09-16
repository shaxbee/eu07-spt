#ifndef SPTCORE_SWITCH_H
#define SPTCORE_SWITCH_H 1

#include <sptCore/SwitchableTracking.h>

namespace sptCore
{

//! \brief Railway 2-way switch
//! \author Zbyszek "ShaXbee" Mandziejewicz
class Switch: public SwitchableTracking
{

public:
    //! Construct switch described by bezier path
    //! \param sector owner
    //! \param p1 common point
    //! \param cp1 common control vector
    //! \param p2 end of straight path
    //! \param cp2 straight path control vector
    //! \param p3 end of diverted path
    //! \param cp3 diverted path control vector
    //! \param position initial position
    Switch(Sector& sector, const osg::Vec3& p1, const osg::Vec3& cp1, const osg::Vec3& p2, const osg::Vec3& cp2, const osg::Vec3& p3, const osg::Vec3& cp3, const std::string& position = "STRAIGHT"); 
    virtual ~Switch();

    virtual const osg::Vec3& getExit(const osg::Vec3& entry) const;
    virtual const Path& getPath(const osg::Vec3& entry) const;

    virtual const ValidPositions getValidPositions() const;

    const Path& getStraightPath() const { return *_straight.first; }
    const Path& getDivertedPath() const { return *_diverted.first; }

protected:
    typedef std::pair<Path*, Path*> PathPair;

    PathPair createBezier(const osg::Vec3& p1, const osg::Vec3& cp1, const osg::Vec3& p2, const osg::Vec3& cp2);

    static ValidPositions _positions;

    PathPair _straight;
    PathPair _diverted;

}; // class Switch

} // namespace sptCore

#endif // headerguard
