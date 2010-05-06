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
    Switch(Sector& sector, std::auto_ptr<Path> straight, std::auto_ptr<Path> diverted, const std::string& position = "STRAIGHT");
    
    template <typename T1, typename T2>
    Switch(Sector& sector, T1* straight, T2* diverted, const std::string& position = "STRAIGHT"): 
        SwitchableTracking(sector), 
        _straight(std::auto_ptr<Path>(straight)), 
        _diverted(std::auto_ptr<Path>(diverted))
    {
        setPosition(position);
    };

    template <typename T1, typename T2>
    Switch(Sector& sector, std::auto_ptr<T1> straight, std::auto_ptr<T2> diverted, const std::string& position = "STRAIGHT"): 
        SwitchableTracking(sector),
        _straight(std::auto_ptr<Path>(straight.release())), 
        _diverted(std::auto_ptr<Path>(diverted.release()))
    {
        setPosition(position);
    };

    virtual ~Switch();

    virtual const osg::Vec3& getExit(const osg::Vec3& entry) const;
    virtual const Path& getPath(const osg::Vec3& entry) const;

    virtual const ValidPositions getValidPositions() const;

    const Path& getStraightPath() const { return *_straight; }
    const Path& getDivertedPath() const { return *_diverted; }

private:
    //PathPair createBezier(const osg::Vec3& p1, const osg::Vec3& cp1, const osg::Vec3& p2, const osg::Vec3& cp2);

    const Path& getStraightReversed() const { return getReversedPath(_straight, _straightReversed); }
    const Path& getDivertedReversed() const { return getReversedPath(_diverted, _divertedReversed); }

    static ValidPositions _positions;

    boost::scoped_ptr<Path> _straight;
    boost::scoped_ptr<Path> _diverted;

    mutable boost::scoped_ptr<Path> _straightReversed;
    mutable boost::scoped_ptr<Path> _divertedReversed;

}; // class Switch

} // namespace sptCore

#endif // headerguard
