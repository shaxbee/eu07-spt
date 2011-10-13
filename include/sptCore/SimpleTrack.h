#ifndef SPTCORE_SIMPLETRACK_H
#define SPTCORE_SIMPLETRACK_H 1

#include "sptCore/Track.h"

#include <memory>

namespace sptCore
{

class SimpleTrack: public Track
{
public:
    template <typename PathT>
    SimpleTrack(const osg::Vec3& sector, PathT path, TrackId front, TrackId back):
        Track(sector), 
        _path(path),
        _front(front),
        _back(back)
    { 
    };

    virtual ~SimpleTrack() { };

    virtual osg::Vec3 getExit(const osg::Vec3& entry) const;
    virtual std::auto_ptr<Path> getPath(const osg::Vec3& entry) const;
    virtual TrackId getNextTrack(const osg::Vec3& entry) const;

    //! \brief Get default (forward) path
    std::auto_ptr<Path> getDefaultPath() const { return _path->clone(); }
    
private:
    std::auto_ptr<Path> _path;
    TrackId _front;
    TrackId _back;
};

}; // namespace sptCore

#endif // headerguard
