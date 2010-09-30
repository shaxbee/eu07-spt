#include <gtest/gtest.h>

#include <boost/array.hpp>

#include <sptCore/Track.h>
#include <sptCore/Sector.h>

namespace sptCore
{
    struct Scenery { };
}

using namespace sptCore;

class SectorTest: public ::testing::Test
{

public:
    SectorTest(): 
        pointA(0, 0, 0),
        pointB(100, 0, 0),
        pointC(200, 0, 0),
        sector(pointA)
    { 
    };

    void setUp()
    {
        std::auto_ptr<Path> path1(new StraightPath(pointA, pointB));
        std::auto_ptr<Path> path2(new StraightPath(pointB, pointC));

        boost::array<RailTracking*, 2> tracks =
        {{
            new Track(sector, path1),
            new Track(sector, path2)
        }};

        boost::array<Sector::Connection, 2> connections =
        {{
            {pointA, NULL, tracks[0]},
            {pointB, tracks[0], tracks[1]}
        }};

        sector.setData(tracks, connections);
    };
    
protected:
    Sector sector;

    const osg::Vec3 pointA;
    const osg::Vec3 pointB;
    const osg::Vec3 pointC;

}; // SectorTest

TEST_F(SectorTest, GetNextTrack)
{
    ASSERT_THROW(sector.getNextTrack(pointA, sector.getRailTracking(0)), Sector::UnknownConnectionException);
    ASSERT_THROW(sector.getNextTrack(pointC, sector.getRailTracking(0)), Sector::UnknownConnectionException);
    ASSERT_THROW(sector.getNextTrack(osg::Vec3(17, 17, 17), sector.getRailTracking(0)), Sector::UnknownConnectionException);

    ASSERT_EQ(&sector.getNextTrack(pointB, sector.getRailTracking(0)), &sector.getRailTracking(1));
    ASSERT_EQ(&sector.getNextTrack(pointB, sector.getRailTracking(1)), &sector.getRailTracking(0));
};

TEST_F(SectorTest, UpdateConnections)
{
    boost::array<Sector::ConnectionUpdate, 1> updates =
    {{
        {pointA, NULL, &sector.getRailTracking(1)}
    }};

    sector.updateConnections(updates);

    ASSERT_EQ(&sector.getNextTrack(pointA, sector.getRailTracking(0)), &sector.getRailTracking(1));
};