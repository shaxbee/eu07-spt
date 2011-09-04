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
    Track(Sector& sector, size_t id, PathT path): RailTracking(sector, id), _path(path) { };

    virtual ~Track() { };

    virtual osg::Vec3 getExit(const osg::Vec3& entry) const;
    virtual std::auto_ptr<Path> getPath(const osg::Vec3& entry) const;

    //! \brief Get default (forward) path
    std::auto_ptr<Path> getDefaultPath() const { return _path->clone(); }
    
private:
    std::auto_ptr<Path> _path;
};

} // namespace sptCore

#endif // headerguard
