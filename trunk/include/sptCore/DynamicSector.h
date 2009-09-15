#ifndef SPTCORE_DYNAMICSECTOR_H
#define SPTCORE_DYNAMICSECTOR_H

#include <sptCore/Sector.h>

#include <map>
#include <set>

namespace sptCore
{

class DynamicSector: public Sector
{

public:
    DynamicSector(Scenery* scenery, osg::Vec3 position): Sector(scenery, position) { };
    virtual ~DynamicSector();

    virtual RailTracking& getNextTrack(const osg::Vec3& position, RailTracking* from) const;
    virtual const Connection& getConnection(const osg::Vec3& position) const;
    virtual size_t getTotalTracks() const { return _tracks.size(); };

    //! \brief Register track at sector
    //! Track instance will be managed by Sector
    void addTrack(RailTracking* track) { _tracks.insert(track); };

    //! \brief Add track at given position
    //! \throw InvalidConnectionException if complementary connection exists at given position 
    void addConnection(const osg::Vec3& position, RailTracking* track);

    //! \brief Add pair of tracks at given position
    //! \throw InvalidConnectionException if complementary connection exists at given position 
    void addConnection(const osg::Vec3& position, RailTracking* left, RailTracking* right);

    class InvalidConnectionException: public boost::exception { };

private:
    typedef std::map<osg::Vec3, Connection> Connections;
    typedef std::set<RailTracking*> Tracks;

    Connections _connections;
    Tracks _tracks;

}; // class sptCore::DynamicSector

} // namespace sptCore

#endif // headerguard
