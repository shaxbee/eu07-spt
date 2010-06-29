#ifndef SPTCORE_TRACK_H
#define SPTCORE_TRACK_H 1

#include <sptCore/RailTracking.h>

#include <memory>

namespace sptCore
{

class Track: public RailTracking
{
public:
    template <typename PathT>
    Track(Sector& sector, PathT path): RailTracking(sector), _forward(path), _backward(_forward->reverse()) { };

    virtual ~Track() { };

    virtual const osg::Vec3& getExit(const osg::Vec3& entry) const;
    virtual const Path& getPath(const osg::Vec3& entry) const;
    virtual const Path& reversePath(const Path& path) const;

    //! \brief Get default (forward) path
    const Path& getDefaultPath() const { return *_forward; }
    
private:
    std::auto_ptr<Path> _forward;
    std::auto_ptr<Path> _backward;
};

} // namespace sptCore

#endif // headerguard
