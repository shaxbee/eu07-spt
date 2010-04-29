#ifndef SPTCORE_DYNAMICSECTOR_H
#define SPTCORE_DYNAMICSECTOR_H

#include <sptCore/Sector.h>

#include <boost/scoped_ptr.hpp>
#include <boost/exception.hpp>

namespace sptCore
{

class DynamicSectorImpl;

//! \brief Modifiable Sector
//! \author Zbyszek "ShaXbee" Mandziejewicz
class DynamicSector: public Sector
{

public:
    DynamicSector(Scenery& scenery, osg::Vec3 position);
    virtual ~DynamicSector();

    virtual const RailTracking& getNextTrack(const osg::Vec3& position, const RailTracking& from) const;
    virtual const Connection& getConnection(const osg::Vec3& position) const;
    virtual size_t getTotalTracks() const;

    //! \brief Register track at sector
    //! Track instance will be managed by Sector
    void addTrack(std::auto_ptr<RailTracking> track);

    //! \brief Unregister track from sector
    void removeTrack(RailTracking& track);

    //! \brief Add track to connection
    //! \throw InvalidConnectionException if complementary connection exists at given position 
    void addConnection(const osg::Vec3& position, const RailTracking& track);

    //! \brief Add connection of tracks pair
    //! \throw InvalidConnectionException if complementary connection exists at given position 
    void addConnection(const osg::Vec3& position, const RailTracking& left, const RailTracking& right);

    //! \brief Remove connection
    void removeConnection(const osg::Vec3& position);

    //! \brief Removed orphaned connections
    //! Search for connections with one or both NULL trackings
    void cleanup();

private:
    boost::scoped_ptr<DynamicSectorImpl> _impl;

}; // class sptCore::DynamicSector

class InvalidConnectionException: public boost::exception { };

} // namespace sptCore

#endif // headerguard
