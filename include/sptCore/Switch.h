#ifndef SPTCORE_SWITCH_H
#define SPTCORE_SWITCH_H 1

#include "sptCore/SwitchableTracking.h"

#include <memory>

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
    Switch(TrackId id, const osg::Vec2f& sector, std::shared_ptr<Path> straight, std::shared_ptr<Path> diverted, TrackId commonId, TrackId straightId, TrackId divertedId, const std::string& position = "STRAIGHT");
    Switch(Switch&& other);
    virtual ~Switch();

    virtual void accept(TrackVisitor& visitor) const;
    virtual osg::Vec3 getExit(const osg::Vec3& entry) const;
    virtual std::shared_ptr<const Path> getPath(const osg::Vec3& entry) const;
    virtual TrackId getNextTrack(const osg::Vec3& entry) const;

    virtual std::vector<std::string> getValidPositions() const;

    std::shared_ptr<const Path> getStraightPath() const;
    std::shared_ptr<const Path> getDivertedPath() const;

private:
    std::shared_ptr<Path> _straight;
    std::shared_ptr<Path> _diverted;

    TrackId _commonId;
    TrackId _straightId;
    TrackId _divertedId;
}; // class Switch

} // namespace sptCore

#endif // headerguard
