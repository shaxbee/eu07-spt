#include <cxxtest/TestSuite.h>

#include <boost/scoped_ptr.hpp>

#include <sptCore/Follower.h>

#include <sptCore/SceneryBuilder.h>
#include <sptCore/DynamicScenery.h>
#include <sptCore/DynamicSector.h>
#include <sptCore/Track.h>

using namespace sptCore;

class FollowerTestSuite: public CxxTest::TestSuite
{

public:
    FollowerTestSuite():
        _point1(Sector::SIZE / 2, Sector::SIZE /2, 0),
        _point2(Sector::SIZE * 1.5, Sector::SIZE / 2, 0),
        _point3(Sector::SIZE / 2, Sector::SIZE * 1.5, 0),
        _point4(-Sector::SIZE / 2, -Sector::SIZE / 2, 0)
    {

    };

    void setUp()
    {

        _builder.reset(new SceneryBuilder());

        _builder->setCurrentSector(osg::Vec3());
        _builder->createTrack("startTrack", _point1, _point2);

        _builder->setCurrentSector(osg::Vec3(Sector::SIZE, 0, 0));
        _builder->createTrack("track2", _point1, _point3);

        _builder->setCurrentSector(osg::Vec3(Sector::SIZE, Sector::SIZE, 0));
        _builder->createTrack("track3", _point1, _point4);

        _builder->cleanup();
        
        _scenery = &_builder->getScenery();

    };

    void testMoveForward()
    {

        Follower follower(_scenery->getTrack("startTrack"), 0.1f);

        follower.move(follower.getPath().length());
        TS_ASSERT_EQUALS(&follower.getSector(), &_scenery->getSector(osg::Vec3(Sector::SIZE, 0, 0)));
        TS_ASSERT_EQUALS(&follower.getTrack(), &_scenery->getTrack("track2"));

        follower.move(follower.getPath().length());
        TS_ASSERT_EQUALS(&follower.getSector(), &_scenery->getSector(osg::Vec3(Sector::SIZE, Sector::SIZE, 0)));
        TS_ASSERT_EQUALS(&follower.getTrack(), &_scenery->getTrack("track3"));

        follower.move(follower.getPath().length());
        TS_ASSERT_EQUALS(&follower.getSector(), &_scenery->getSector(osg::Vec3(0, 0, 0)));
        TS_ASSERT_EQUALS(&follower.getTrack(), &_scenery->getTrack("startTrack"));
        
    };

    void testMoveBackward()
    {

        Follower follower(_scenery->getTrack("startTrack"), 0.1f);

        follower.move(-follower.getPath().length());
        TS_ASSERT_EQUALS(&follower.getSector(), &_scenery->getSector(osg::Vec3(Sector::SIZE, Sector::SIZE, 0)));
        TS_ASSERT_EQUALS(&follower.getTrack(), &_scenery->getTrack("track3"));

        follower.move(-follower.getPath().length());
        TS_ASSERT_EQUALS(&follower.getSector(), &_scenery->getSector(osg::Vec3(Sector::SIZE, 0, 0)));
        TS_ASSERT_EQUALS(&follower.getTrack(), &_scenery->getTrack("track2"));

        follower.move(-follower.getPath().length());
        TS_ASSERT_EQUALS(&follower.getSector(), &_scenery->getSector(osg::Vec3(0, 0, 0)));
        TS_ASSERT_EQUALS(&follower.getTrack(), &_scenery->getTrack("startTrack"));

    };

    void testGetPosition()
    {

        const Path& path = _scenery->getTrack("startTrack").getDefaultPath();
        Follower follower(_scenery->getTrack("startTrack")); 

        // Begining of track
        TS_ASSERT_EQUALS(follower.getPosition(), path.front());

        // 1/2 of track
        follower.move(path.length() * 0.5);
        TS_ASSERT_EQUALS(follower.getPosition(), path.front() * 0.5 + path.back() * 0.5);

        // 3/4 of track
        follower.move(path.length() * 0.25);
        TS_ASSERT_EQUALS(follower.getPosition(), path.front() * 0.25 + path.back() * 0.75);

        // End of track
        follower.move(path.length() * 0.25);
        TS_ASSERT_EQUALS(follower.getPosition(), path.back());

    }; 

private:
    boost::scoped_ptr<SceneryBuilder> _builder;
    DynamicScenery* _scenery;

    osg::Vec3 _point1;
    osg::Vec3 _point2;
    osg::Vec3 _point3;
    osg::Vec3 _point4;

}; // class FollowerTestSuite
