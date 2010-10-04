#include <gtest/gtest.h>

#include <boost/array.hpp>
#include <osg/io_utils>

#include <sptCore/Scenery.h>

#include <sptCore/Track.h>
#include <sptCore/Switch.h>
#include <sptCore/Sector.h>

using namespace sptCore;

class SceneryTest: public ::testing::Test
{
public:
    SceneryTest(): dummy(0.0f, 0.0f, 0.0f), sector(dummy) { };
    
protected:
    Scenery scenery;
    Sector sector;
    osg::Vec3 dummy;
    
}; // class SceneryTestSuite

TEST_F(SceneryTest, TrackAccess)
{
    std::auto_ptr<Track> testTrack(new Track(sector, new StraightPath(dummy, dummy)));

    scenery.addTrack("track1", *testTrack);

    ASSERT_EQ(&scenery.getTrack("track1"), testTrack.get());
    ASSERT_THROW(&scenery.getTrack("track2"), SceneryException);
};

TEST_F(SceneryTest, SwitchAccess)
{
    std::auto_ptr<Switch> testSwitch(new Switch(sector, new StraightPath(dummy, dummy), new StraightPath(dummy, dummy)));

    scenery.addSwitch("switch1", *testSwitch);
    
    ASSERT_EQ(&scenery.getSwitch("switch1"), testSwitch.get());
    ASSERT_THROW(&scenery.getSwitch("switch2"), SceneryException);
};

TEST_F(SceneryTest, AddSector)
{
    osg::Vec3f leftPos(0.0f, 0.0f, 0.0f);
    osg::Vec3f rightPos(Sector::SIZE, 0.0f, 0.0f);

    osg::Vec3f beginInternal(0.0f, 0.0f, 0.0f);
    osg::Vec3f endInternal(Sector::SIZE - 200.0f, 1.0f, 0.0f);
    osg::Vec3f beginExternal(-200.0f, 1.0f, 0.0f);
    osg::Vec3f endExternal(100.0f, 1.0f, 0.0f);

    {
        std::auto_ptr<Sector> left(new Sector(leftPos));
        {
            boost::array<RailTracking*, 1> tracks = {{ new Track(*left, new StraightPath(beginInternal, endInternal)) }};
            boost::array<Sector::Connection, 1> connections = {{ {endInternal, tracks[0], NULL} }};

            left->setData(tracks, connections);
        };

        std::auto_ptr<Sector> right(new Sector(rightPos));
        {
            boost::array<RailTracking*, 1> tracks = {{ new Track(*right, new StraightPath(beginExternal, endExternal)) }};
            boost::array<Sector::Connection, 1> connections = {{ {beginExternal, tracks[0], NULL} }};

            right->setData(tracks, connections);
        }

        scenery.addSector(left);
        scenery.addSector(right);
    };

    const Sector& left = scenery.getSector(leftPos);
    const Sector& right = scenery.getSector(rightPos);

    ASSERT_EQ(&left.getNextTrack(endInternal, left.getRailTracking(0)), &right.getRailTracking(0));
    ASSERT_EQ(&right.getNextTrack(beginExternal, right.getRailTracking(0)), &left.getRailTracking(0));

    scenery.removeSector(rightPos);
    ASSERT_THROW(left.getNextTrack(endInternal, left.getRailTracking(0)), Sector::UnknownConnectionException);
};