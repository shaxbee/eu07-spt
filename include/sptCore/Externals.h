#ifndef SPTCORE_EXTERNALS_H
#define SPTCORE_EXTERNALS_H 1

#include <memory>
#include <utility>
#include <vector>

#include <osg/Vec2f>
#include <osg/Vec3f>

#include "sptCore/Sector.h"

namespace sptCore
{

class TrackQuery;
class ExternalsImpl;

class Externals
{
public:
    typedef std::vector<std::pair<osg::Vec3f, TrackId> > Entries;

    std::pair<osg::Vec2f, TrackId> getNextTrack(const TrackQuery& query) const;
    void add(const osg::Vec2f& sector, Entries entries);

private:
    std::unique_ptr<ExternalsImpl> _impl;    
}; // class Externals

}; // namespace sptCore

#endif
