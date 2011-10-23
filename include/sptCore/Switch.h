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
    Switch(const osg::Vec3f& sector, T1 straight, T2 diverted, TrackId commonId, TrackId straightId, TrackId divertedId, const std::string& position = "STRAIGHT"):
        SwitchableTracking(sector),
        _straight(straight),
        _diverted(diverted),
        _commonId(commonId),
        _straightId(straightId),
        _divertedId(divertedId)
    {
        setPosition(position);
    };

    virtual ~Switch() { };

    virtual void accept(TrackVisitor& visitor) const;
    virtual osg::Vec3 getExit(const osg::Vec3& entry) const;
    virtual std::auto_ptr<Path> getPath(const osg::Vec3& entry) const;
    virtual TrackId getNextTrack(const osg::Vec3& entry) const;

    virtual const ValidPositions& getValidPositions() const;

    std::auto_ptr<Path> getStraightPath() const { return _straight->clone(); }
    std::auto_ptr<Path> getDivertedPath() const { return _diverted->clone(); }

private:
    std::auto_ptr<Path> _straight;
    std::auto_ptr<Path> _diverted;

    TrackId _commonId;
    TrackId _straightId;
    TrackId _divertedId;
}; // class Switch

} // namespace sptCore

#endif // headerguard
