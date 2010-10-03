#include <gtest/gtest.h>

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