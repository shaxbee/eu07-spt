#ifndef SPTCORE_SECTOR_H
#define SPTCORE_SECTOR_H 1

#include <vector>
#include <memory>

#include <osg/Vec3f>

#include "sptCore/Track.h"

namespace sptCore
{

typedef std::vector<std::unique_ptr<Track>> Tracks;

class TrackVisitor;

//! Container for rail trackings located in chunk of Scenery
//! \author Zbigniew "ShaXbee" Mandziejewicz
class Sector
{
public:
    Sector(const osg::Vec2f& position, Tracks&& tracks);

    const osg::Vec2f& getPosition() const { return _position; };
    const osg::Vec2f& getSize() const;
    const Track& getTrack(const TrackId index) const;

    void accept(TrackVisitor& visitor) const;

    static float SIZE;

private:
    const osg::Vec2f _position;
    Tracks _tracks;
}; // class sptCore::Sector

} // namespace sptCore

#endif // header guard
