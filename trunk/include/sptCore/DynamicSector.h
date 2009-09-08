#ifndef SPTCORE_DYNAMICSECTOR_H
#define SPTCORE_DYNAMICSECTOR_H

#include <sptCore/Sector.h>

#include <map>

namespace sptCore
{

class DynamicSector: public Sector
{

public:
    DynamicSector(osg::Vec3 position): Sector(position) { };

    virtual RailTracking* getNextTrack(const osg::Vec3& position, RailTracking* from) const;
    virtual Connection getConnection(const osg::Vec3& position) const;

    //! \brief Add track at given position
    //! \throw InvalidConnectionException if complementary connection exists at given position 
    void addTrack(RailTracking* track, const osg::Vec3& position);

    //! \brief Add pair of tracks at given position
    //! \throw InvalidConnectionException if complementary connection exists at given position 
    void addConnection(RailTracking* left, RailTracking* right, const osg::Vec3& position);

    class InvalidConnectionException: public boost::exception { };

private:
    typedef std::map<osg::Vec3, Connection> Connections;
    Connections _connections;

}; // class sptCore::DynamicSector

} // namespace sptCore

#endif // headerguard
