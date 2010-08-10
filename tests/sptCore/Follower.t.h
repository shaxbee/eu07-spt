#include <cxxtest/TestSuite.h>

#include <boost/scoped_ptr.hpp>
#include <boost/array.hpp>

#include <sptCore/Follower.h>

#include <sptCore/Scenery.h>
#include <sptCore/Sector.h>
#include <sptCore/Track.h>

using namespace sptCore;

namespace
{

template <typename TracksContainerT>
void set_sector_data(Sector& sector, TracksContainerT& data, size_t index)
{
    boost::array<RailTracking*, 1> trackings = 
    {{ 
        data[index] 
    }};

    Track* left = data[index ? (index - 1) : 2 % 3];
    Track* center = data[index];
    Track* right = data[(index + 1) % 3];

    osg::Vec3f front(center->getDefaultPath().front());
    osg::Vec3f back(center->getDefaultPath().back());

    boost::array<Sector::Connection, 2> connections =
    {{
        {front, left, center},
        {back, center, right}
    }};

    std::sort(connections.begin(), connections.end(), ConnectionLess());

    sector.setData(trackings, connections);
};


}

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
        _scenery.reset(new Scenery());

        std::auto_ptr<Sector> sector1(new Sector(osg::Vec3d(0, 0, 0)));  
        std::auto_ptr<Sector> sector2(new Sector(osg::Vec3d(Sector::SIZE, 0, 0)));
        std::auto_ptr<Sector> sector3(new Sector(osg::Vec3d(Sector::SIZE, Sector::SIZE, 0)));
        
        boost::array<Track*, 3> tracks = 
        {{ 
            new Track(*sector1, new StraightPath(_point1, _point2)),
            new Track(*sector2, new StraightPath(_point1, _point3)),
            new Track(*sector3, new StraightPath(_point1, _point4))
        }};

        set_sector_data(*sector1, tracks, 0);
        set_sector_data(*sector2, tracks, 1);
        set_sector_data(*sector3, tracks, 2);

        _scenery->addSector(sector1);
        _scenery->addSector(sector2);
        _scenery->addSector(sector3);

        _scenery->addTrack("track1", *tracks[0]);
        _scenery->addTrack("track2", *tracks[1]);
        _scenery->addTrack("track3", *tracks[2]);
    };

    void testMoveForward()
    {
        Follower follower(_scenery->getTrack("track1"), 0.1f);

        follower.move(follower.getPath().length());
        TS_ASSERT_EQUALS(&follower.getSector(), &_scenery->getSector(osg::Vec3(Sector::SIZE, 0, 0)));
        TS_ASSERT_EQUALS(&follower.getTrack(), &_scenery->getTrack("track2"));

        follower.move(follower.getPath().length());
        TS_ASSERT_EQUALS(&follower.getSector(), &_scenery->getSector(osg::Vec3(Sector::SIZE, Sector::SIZE, 0)));
        TS_ASSERT_EQUALS(&follower.getTrack(), &_scenery->getTrack("track3"));

        follower.move(follower.getPath().length());
        TS_ASSERT_EQUALS(&follower.getSector(), &_scenery->getSector(osg::Vec3(0, 0, 0)));
        TS_ASSERT_EQUALS(&follower.getTrack(), &_scenery->getTrack("track1"));
    };

    void testMoveBackward()
    {

        Follower follower(_scenery->getTrack("track1"), 0.1f);

        follower.move(-follower.getPath().length());
        TS_ASSERT_EQUALS(&follower.getSector(), &_scenery->getSector(osg::Vec3(Sector::SIZE, Sector::SIZE, 0)));
        TS_ASSERT_EQUALS(&follower.getTrack(), &_scenery->getTrack("track3"));

        follower.move(-follower.getPath().length());
        TS_ASSERT_EQUALS(&follower.getSector(), &_scenery->getSector(osg::Vec3(Sector::SIZE, 0, 0)));
        TS_ASSERT_EQUALS(&follower.getTrack(), &_scenery->getTrack("track2"));

        follower.move(-follower.getPath().length());
        TS_ASSERT_EQUALS(&follower.getSector(), &_scenery->getSector(osg::Vec3(0, 0, 0)));
        TS_ASSERT_EQUALS(&follower.getTrack(), &_scenery->getTrack("track1"));

    };

    void testGetPosition()
    {

        const Path& path = _scenery->getTrack("track1").getDefaultPath();
        Follower follower(_scenery->getTrack("track1")); 

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
    boost::scoped_ptr<Scenery> _scenery;

    osg::Vec3 _point1;
    osg::Vec3 _point2;
    osg::Vec3 _point3;
    osg::Vec3 _point4;

}; // class FollowerTestSuite
