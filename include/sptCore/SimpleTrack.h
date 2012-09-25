#ifndef SPTCORE_SIMPLETRACK_H
#define SPTCORE_SIMPLETRACK_H 1

#include "sptCore/Track.h"

#include <memory>

namespace sptCore
{

class SimpleTrack: public Track
{
public:
    SimpleTrack(const osg::Vec2f& sector, std::shared_ptr<Path> path, TrackId front, TrackId back);
    SimpleTrack(SimpleTrack&& other);

    virtual ~SimpleTrack();

    virtual void accept(TrackVisitor& visitor) const;
    virtual osg::Vec3 getExit(const osg::Vec3& entry) const;
    virtual std::shared_ptr<const Path> getPath(const osg::Vec3& entry) const;
    virtual TrackId getNextTrack(const osg::Vec3& entry) const;

    //! \brief Get default (forward) path
    std::shared_ptr<const Path> getDefaultPath() const;
    
private:
    std::shared_ptr<Path> _path;
    TrackId _front;
    TrackId _back;
};

}; // namespace sptCore

#endif // headerguard
