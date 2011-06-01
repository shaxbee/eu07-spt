#ifndef SPTCORE_SWITCH_H
#define SPTCORE_SWITCH_H 1

#include <boost/scoped_ptr.hpp>

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
    //! \param straight straight path
    //! \param diverted diverted path
    //! \param position initial position
    template <typename T1, typename T2>
    Switch(Sector& sector, T1 straight, T2 diverted, const std::string& position = "STRAIGHT"):
        SwitchableTracking(sector),
        _straight(straight),
        _diverted(diverted),
        _straightReversed(_straight->reverse()),
        _divertedReversed(_diverted->reverse())
    {
        setPosition(position);
    };

    virtual ~Switch() { };

    virtual const osg::Vec3& getExit(const osg::Vec3& entry) const;
    virtual const Path& getPath(const osg::Vec3& entry) const;
    virtual const Path& reversePath(const Path& path) const;

    virtual const ValidPositions& getValidPositions() const;

    const Path& getStraightPath() const { return *_straight; }
    const Path& getDivertedPath() const { return *_diverted; }

private:
    //PathPair createBezier(const osg::Vec3& p1, const osg::Vec3& cp1, const osg::Vec3& p2, const osg::Vec3& cp2);

    static ValidPositions _positions;

    std::auto_ptr<Path> _straight;
    std::auto_ptr<Path> _diverted;
    std::auto_ptr<Path> _straightReversed;
    std::auto_ptr<Path> _divertedReversed;

}; // class Switch

} // namespace sptCore

#endif // headerguard
