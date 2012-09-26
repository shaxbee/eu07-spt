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

std::unique_ptr<Track> makeSimpleTrack(size_t id, osg::Vec2f sector, osg::Vec3f front, osg::Vec3f back, TrackId frontId, TrackId backId)
{
    return std::unique_ptr<Track>(new SimpleTrack(
        TrackId(id), 
        sector,
        std::make_shared<StraightPath>(front, back),
        frontId, backId
    ));
};    

Tracks makeDummyTracks(size_t count)
{
    Tracks result;

    while(count--)
    {
        result.push_back(std::unique_ptr<Track>(new SimpleTrack(
            TrackId(result.size()),
            osg::Vec2f(),
            std::make_shared<StraightPath>(osg::Vec3f(), osg::Vec3f()),
            TrackId::null(),
            TrackId::null()
        )));
    };
    
    return std::move(result);        
};        

TEST_F(SceneryTest, Aliases)
{
    scenery.addSector(Sector(osg::Vec2f(), makeDummyTracks(1))); //std::move(tracks)));
    scenery.addAliases(osg::Vec2f(), {{std::string("track1"), TrackId(0)}});

    ASSERT_NO_THROW(scenery.getTrack("track1"));
    ASSERT_THROW(scenery.getTrack("track2"), std::out_of_range);
    ASSERT_THROW(scenery.getSwitch("track1"), std::bad_cast);
};

TEST_F(SceneryTest, NextTrack)
{
    osg::Vec3f common(10.0f, 0.0f, 0.0f);

    Tracks tracks;
    tracks.push_back(makeSimpleTrack(0, osg::Vec2f(), osg::Vec3f(0.0f, 0.0f, 0.0f), common, TrackId::null(), TrackId(1)));
    tracks.push_back(makeSimpleTrack(1, osg::Vec2f(), common, osg::Vec3f(20.0f, 0.0f, 0.0f), TrackId(0), TrackId::null()));

    scenery.addSector(Sector(osg::Vec2f(), std::move(tracks)));

    const Sector& sector = scenery.getSector(osg::Vec2f());

    ASSERT_EQ(TrackId(1), scenery.getNextTrack(sector.getTrack(TrackId(0)), common).getId());
    ASSERT_EQ(TrackId(0), scenery.getNextTrack(sector.getTrack(TrackId(1)), common).getId());
    ASSERT_THROW(scenery.getNextTrack(sector.getTrack(TrackId(0)), osg::Vec3f(0.0f, 0.0f, 0.0f)), std::runtime_error);
};     

TEST_F(SceneryTest, Externals)
{
    // sector A
    const osg::Vec2f sectorA(0.0f, 0.0f);
    const osg::Vec3f externalA(1800.0f, 0.0f, 0.0f);
    {
        Tracks tracks;
        tracks.push_back(makeSimpleTrack(
            0,
            sectorA, 
            osg::Vec3f(0.0f, 0.0f, 0.0f), externalA, 
            TrackId::null(), TrackId::external()
        ));

        scenery.addSector(Sector(sectorA, std::move(tracks)));
        scenery.addExternals(sectorA, {{externalA, TrackId(0)}});
    };
    
    // sector B
    const osg::Vec2f sectorB(2000.0f, 0.0f);
    const osg::Vec3f externalB(-200.0f, 0.0f, 0.0f);
    {
        Tracks tracks;
        tracks.push_back(makeSimpleTrack(
            0,
            sectorB,
            externalB, 
            osg::Vec3f(200.0f, 0.0f, 0.0f), 
            TrackId::external(), TrackId::null()
        ));
        
        scenery.addSector(Sector(sectorB, std::move(tracks)));
        scenery.addExternals(sectorB, {{externalB, TrackId(0)}});
    };

    // get track externally connected to trackA
    const Track& trackB = scenery.getNextTrack(scenery.getSector(sectorA).getTrack(TrackId(0)), externalA);

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
