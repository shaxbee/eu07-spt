#ifndef SPTCORE_EXTERNALS_H
#define SPTCORE_EXTERNALS_H 1

#include <memory>
#include <utility>
#include <vector>
#include <unordered_map>

#include <osg/Vec2f>
#include <osg/Vec3f>

#include "sptCore/TrackLocator.h"

namespace sptCore
{


class Externals
{
public:
    TrackLocator getNextTrack(const osg::Vec2f& sector, const osg::Vec3f& position) const;

    void add(const osg::Vec2f& sector, std::vector<std::pair<osg::Vec3f, TrackId>> entries);

private:
    typedef std::pair<osg::Vec2f, osg::Vec3f> Location;

    struct LocationHash
    {
        std::size_t operator()(const Location& value) const;
    };
     
    std::unordered_map<Location, std::pair<TrackLocator, TrackLocator>, LocationHash> _grid;
}; // class Externals

}; // namespace sptCore

#endif
