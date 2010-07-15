#ifndef SPTCORE_SECTOR_H
#define SPTCORE_SECTOR_H 1

#include <vector>

#include <boost/ptr_container/ptr_vector.hpp>

#include <osg/Vec3f>
#include <osg/Vec3d>

#include "sptCore/RailTracking.h"

namespace sptCore
{

class Scenery;

class Sector
{

public:
    Sector(Scenery& scenery, const osg::Vec3d& position);

    const Scenery& getScenery() const { return _scenery; };
    const osg::Vec3d& getPosition() const { return _position; };
    
    template <typename RailTrackingContainerT, typename ConnectionContainerT>
    void setData(RailTrackingContainerT& trackings, const ConnectionContainerT& connections);

    //! Get other track connected at given position
    //!
    //! \throw UnknownConnectionException if there is no connection at given position
    const RailTracking& getNextTrack(const osg::Vec3& position, const RailTracking& from) const;

    const RailTracking& getRailTracking(size_t index) const;

    size_t getTracksCount() const;

    //! Update track connections
    //!
    //! \param connections Container of ConnectionUpdate
    template <typename ContainerT>
    void updateConnections(const ContainerT& connections); 

    struct Connection
    {
        osg::Vec3f position;
        const RailTracking* first;
        const RailTracking* second;
    };

    struct ConnectionUpdate
    {
        osg::Vec3f position;
        const RailTracking* previous;
        const RailTracking* current;
    };

    typedef boost::error_info<struct tag_position, osg::Vec3f> PositionInfo;
    class UnknownConnectionException: public boost::exception { };

    static float SIZE;

private:
    typedef std::vector<Connection> Connections;
    typedef boost::ptr_vector<RailTracking> RailTrackings;

    Scenery& _scenery;
    const osg::Vec3d _position;

    Connections _connections;
    RailTrackings _trackings;

}; // class sptCore::Sector

struct ConnectionLess
{
    bool operator()(const Sector::Connection& left, const Sector::Connection& right) const { return left.position < right.position; }
}; // struct sptCore::ConnectionLess

namespace
{

    struct ConnectionGreater
    {
        bool operator()(const Sector::Connection& left, const Sector::Connection& right) const { return right.position < left.position; }
    }; // struct ::ConnectionGreater

    template <typename RailTrackingContainerT>
    void transferTrackings(RailTrackingContainerT& source, boost::ptr_vector<RailTracking>& dest)
    {
        for(typename RailTrackingContainerT::iterator iter = source.begin(); iter != source.end(); iter++)
            dest.push_back(*iter);
    };

    template <>
    void transferTrackings(boost::ptr_vector<RailTracking>& source, boost::ptr_vector<RailTracking>& dest)
    {
        dest.transfer(dest.begin(), source);
    };

}; // anonymous namespace

template <typename RailTrackingContainerT, typename ConnectionContainerT>
void Sector::setData(RailTrackingContainerT& trackings, const ConnectionContainerT& connections)
{
    assert(_trackings.empty() && _connections.empty() && "Data already set");

    _trackings.reserve(trackings.size());
    transferTrackings(trackings, _trackings);

    assert(std::adjacent_find(connections.begin(), connections.end(), ConnectionGreater()) == connections.end() && "Invalid connections order");

    _connections.reserve(connections.size());
    std::copy(connections.begin(), connections.end(), std::back_inserter(_connections));
}; // Sector::Sector(tracking, connections)

template <typename ContainerT>
void Sector::updateConnections(const ContainerT& connections)
{
    Connections::iterator dest = _connections.begin();

    for(typename ContainerT::const_iterator iter = connections.begin(); iter != connections.end(); iter++)
    {
        Connection search = {iter->position, NULL, NULL};
        dest = std::lower_bound(dest, _connections.end(), search, ConnectionLess());

        if(dest == _connections.end() || iter->position != dest->position)
            throw std::logic_error("Connection not found");

        if(dest->first != iter->previous && dest->second != iter->previous)
            throw std::logic_error("RailTracking not found");

        if(dest->first == iter->previous)
        {
            dest->first = iter->current;
        }
        else
        {
            dest->second = iter->current;
        };
    };
};

} // namespace sptCore

#endif // headerguard
