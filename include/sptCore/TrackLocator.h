#ifndef SPTCORE_TRACKLOCATOR_H
#define SPTCORE_TRACKLOCATOR_H 1

#include <stdint.h>
#include <osg/Vec2f>

namespace sptCore
{

class TrackId
{
public:
    explicit TrackId(uint32_t value);

    bool operator==(TrackId other) const;

    bool isNull() const;
    bool isExternal() const;

    uint32_t value() const;

    static TrackId null();
    static TrackId external();

private:
    uint32_t _value;
};

struct TrackLocator
{
    osg::Vec2f sector;
    TrackId id;
};

}; // namespace sptCore

#endif
