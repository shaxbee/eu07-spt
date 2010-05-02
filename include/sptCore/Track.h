#ifndef SPTCORE_TRACK_H
#define SPTCORE_TRACK_H 1

#include <sptCore/RailTracking.h>

#include <boost/scoped_ptr.hpp>

namespace sptCore
{

class Track: public RailTracking
{

public:
    //! Construct straight track
    template <typename T>
    Track(Sector& sector, T* path): RailTracking(sector), _forward(path) { };

    template <typename T>
    Track(Sector& sector, std::auto_ptr<T>& path): RailTracking(sector), _forward(path.release()) { };

    virtual ~Track() { };

    virtual const osg::Vec3& getExit(const osg::Vec3& entry) const;
    virtual const Path& getPath(const osg::Vec3& entry) const;

    //! \brief Get default (forward) path
    const Path& getDefaultPath() const { return *_forward; }
    
private:
    const Path& getReversedPath() const { return RailTracking::getReversedPath(_forward, _backward); }

    boost::scoped_ptr<Path> _forward;
    mutable boost::scoped_ptr<Path> _backward;

};

} // namespace sptCore

#endif // headerguard
