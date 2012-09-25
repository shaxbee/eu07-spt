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

    bool operator==(const TrackId& other) const;
    operator bool() const;

    bool isExternal() const;

    uint32_t value() const { return _value; }

    static TrackId null();
    static TrackId external();

private:
    uint32_t _value;
};

class TrackLocator
{
public:
    TrackLocator(const osg::Vec2f& sector, TrackId id);

    bool operator==(const TrackLocator& other) const;
    operator bool() const;

    const osg::Vec2f& sector() const { return _sector; }
    const TrackId& id() const { return _id; }

    static TrackLocator null();

private:    
    osg::Vec2f _sector;
    TrackId _id;
};

}; // namespace sptCore

#endif
