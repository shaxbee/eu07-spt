#include <gtest/gtest.h>

#include <boost/array.hpp>
#include <osg/io_utils>

#include <sptCore/Scenery.h>

#include <sptCore/SimpleTrack.h>
#include <sptCore/Switch.h>
#include <sptCore/Sector.h>

using namespace sptCore;

class SceneryTest: public ::testing::Test
{
public:
    SceneryTest(): dummy(0.0f, 0.0f, 0.0f) { };
    
protected:
    Scenery scenery;
    osg::Vec3 dummy;
    
}; // class SceneryTestSuite

TEST_F(SceneryTest, TrackAccess)
{
    std::auto_ptr<SimpleTrack> testTrack(new SimpleTrack(dummy, new StraightPath(dummy, dummy), TrackId::null(), TrackId::null()));

    scenery.addTrack("track1", *testTrack);

    ASSERT_EQ(&scenery.getTrack("track1"), testTrack.get());
    ASSERT_THROW(&scenery.getTrack("track2"), SceneryException);
};

TEST_F(SceneryTest, SwitchAccess)
{
    std::auto_ptr<Switch> testSwitch(new Switch(dummy, new StraightPath(dummy, dummy), new StraightPath(dummy, dummy), TrackId::null(), TrackId::null(), TrackId::null()));

    scenery.addSwitch("switch1", *testSwitch);
    
    ASSERT_EQ(&scenery.getSwitch("switch1"), testSwitch.get());
    ASSERT_THROW(&scenery.getSwitch("switch2"), SceneryException);
};

#if 0
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
            boost::array<Track*, 1> tracks = {{ new Track(*left, new StraightPath(beginInternal, endInternal)) }};
            boost::array<Connection, 1> connections = {{ {endInternal, tracks[0], NULL} }};
            boost::array<ExternalConnection, 1> externals = {{ {leftPos, endInternal, 0} }};

            left->setData(tracks, connections, externals);
        };

        std::auto_ptr<Sector> right(new Sector(rightPos));
        {
            boost::array<Track*, 1> tracks = {{ new Track(*right, new StraightPath(beginExternal, endExternal)) }};
            boost::array<Connection, 1> connections = {{ {beginExternal, tracks[0], NULL} }};
            boost::array<ExternalConnection, 1> externals = {{ {rightPos, beginExternal, 0} }};

            right->setData(tracks, connections, externals);
        }

        scenery.addSector(left);
        scenery.addSector(right);
    };

    const Sector& left = scenery.getSector(leftPos);
    const Sector& right = scenery.getSector(rightPos);

    ASSERT_EQ(&left.getNextTrack(endInternal, left.getTrack(0)), &right.getTrack(0));
    ASSERT_EQ(&right.getNextTrack(beginExternal, right.getTrack(0)), &left.getTrack(0));

    scenery.removeSector(rightPos);
    ASSERT_THROW(left.getNextTrack(endInternal, left.getTrack(0)), Sector::UnknownConnectionException);
};
#endif
