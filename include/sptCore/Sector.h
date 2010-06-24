#ifndef SPTCORE_SECTOR_H
#define SPTCORE_SECTOR_H 1

#include <osg/Vec3>
#include <vector>
#include <boost/ptr_container/ptr_vector.hpp>

#include "sptCore/RailTracking.h"

namespace sptCore
{

class Sector
{

public:
    template <typename RailTrackingContainerT, typename ConnectionContainerT>
    Sector(RailTrackingContainerT& trackings, const ConnectionContainerT& connections);

    const RailTracking& getNextTrack(const osg::Vec3& position, const RailTracking& from) const;
    size_t getTracksCount() const;

    template <typename ContainerT>
    void updateConnections(const ContainerT& connections); 

    struct Connection
    {
        osg::Vec3 position;
        RailTracking* first;
        RailTracking* second;
    };

    struct ConnectionUpdate
    {
        osg::Vec3 position;
        RailTracking* tracking;
    };

    static float SIZE;

private:
    typedef std::vector<Connection> Connections;
    typedef boost::ptr_vector<RailTracking> RailTrackings;

    Connections _connections;
    RailTrackings _trackings;

}; // class sptCore::Sector

namespace
{

struct ConnectionGreater
{
    bool operator()(const Sector::Connection& left, const Sector::Connection& right) const { return right.position < left.position; }
}; // struct ::ConnectionGreater

struct ConnectionLess
{
    bool operator()(const Sector::Connection& left, const Sector::Connection& right) const { return left.position < right.position; }
}; // struct ::ConnectionLess

}; // anonymous namespace

template <typename RailTrackingContainerT, typename ConnectionContainerT>
Sector::Sector(RailTrackingContainerT& trackings, const ConnectionContainerT& connections)
{
    _trackings = trackings.release();

    // check if connections are sorted
    assert(std::adjacent_find(connections.begin(), connections.end(), ConnectionGreater()) == connections.end() && "Invalid connections order");

    _connections.reserve(connections.size());
    std::copy(connections.begin(), connections.end(), std::back_inserter(connections));
}; // Sector::Sector(tracking, connections)

template <typename ContainerT>
void Sector::updateConnections(const ContainerT& connections)
{
    Connections::iterator dest = _connections.begin();

    for(typename ContainerT::const_iterator iter = connections.begin(); iter != connections.end(); iter++)
    {
        Connections::iterator dest = std::lower_bound(dest, _connections.end(), *iter, ConnectionLess());

        assert(dest != _connections.end());
        assert(iter.first == dest->position);
        assert(!iter->first || !iter->second);

        if(!dest->first)
        {
            dest->first = iter->tracking;
        }
        else
        {
            dest->second = iter->tracking;
        };
    };
};

} // namespace sptCore

#endif // headerguard
