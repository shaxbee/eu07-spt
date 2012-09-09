#ifndef SPTCORE_EXTERNALS_H
#define SPTCORE_EXTERNALS_H 1

#include <memory>
#include <utility>
#include <vector>

#include <osg/Vec2f>
#include <osg/Vec3f>

#include "sptCore/TrackLocator.h"

namespace sptCore
{

class ExternalsState;

class Externals
{
public:
    TrackLocator getNextTrack(const osg::Vec2f& sector, const osg::Vec3f& position, const TrackId from) const;

    void add(const osg::Vec2f& sector, std::vector<std::pair<osg::Vec3f, TrackId>> entries);

private:
    std::unique_ptr<ExternalsState> _state;    
}; // class Externals

}; // namespace sptCore

#endif
