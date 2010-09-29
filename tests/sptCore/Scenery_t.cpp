#include <gtest/gtest.h>

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

    ASSERT_EQ(&_scenery.getTrack("track1"), testTrack.get());
    ASSERT_THROW(&_scenery.getTrack("track2"), SceneryException);
};

TEST_F(SceneryTest, SwitchAccess)
{
    std::auto_ptr<Switch> testSwitch(new Switch(sector, new StraightPath(dummy, dummy), new StraightPath(dummy, dummy)));

    scenery.addSwitch("switch1", *testSwitch);
    
    TS_ASSERT_EQS(&_scenery->getSwitch("switch1"), testSwitch.get());
    TS_ASSERT_THROWS(&_scenery->getSwitch("switch2"), SceneryException);
};