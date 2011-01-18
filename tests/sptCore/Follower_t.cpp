#include <gtest/gtest.h>

#include <boost/scoped_ptr.hpp>
#include <boost/array.hpp>

#include <osg/io_utils>

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

    boost::array<Connection, 2> connections =
    {{
        {front, left, center},
        {back, center, right}
    }};

    std::sort(connections.begin(), connections.end(), ConnectionLess());

    boost::array<ExternalConnection, 0> externals;

    sector.setData(trackings, connections, externals);
};

}

class FollowerTest: public ::testing::Test
{

public:
    void SetUp()
    {
        point1 = osg::Vec3(Sector::SIZE / 2, Sector::SIZE /2, 0);
        point2 = osg::Vec3(Sector::SIZE * 1.5, Sector::SIZE / 2, 0);
        point3 = osg::Vec3(Sector::SIZE / 2, Sector::SIZE * 1.5, 0);
        point4 = osg::Vec3(-Sector::SIZE / 2, -Sector::SIZE / 2, 0);

        std::auto_ptr<Sector> sector1(new Sector(osg::Vec3d(0, 0, 0)));  
        std::auto_ptr<Sector> sector2(new Sector(osg::Vec3d(Sector::SIZE, 0, 0)));
        std::auto_ptr<Sector> sector3(new Sector(osg::Vec3d(Sector::SIZE, Sector::SIZE, 0)));
        
        boost::array<Track*, 3> tracks = 
        {{ 
            new Track(*sector1, new StraightPath(point1, point2)),
            new Track(*sector2, new StraightPath(point1, point3)),
            new Track(*sector3, new StraightPath(point1, point4))
        }};

        set_sector_data(*sector1, tracks, 0);
        set_sector_data(*sector2, tracks, 1);
        set_sector_data(*sector3, tracks, 2);

        scenery.addSector(sector1);
        scenery.addSector(sector2);
        scenery.addSector(sector3);

        scenery.addTrack("track1", *tracks[0]);
        scenery.addTrack("track2", *tracks[1]);
        scenery.addTrack("track3", *tracks[2]);
    };
    
protected:
    Scenery scenery;

    osg::Vec3 point1;
    osg::Vec3 point2;
    osg::Vec3 point3;
    osg::Vec3 point4;

};

TEST_F(FollowerTest, moveForward)
{
    Follower follower(scenery.getTrack("track1"), 0.1f);

    follower.move(follower.getPath().length());
    ASSERT_EQ(&follower.getSector(), &scenery.getSector(osg::Vec3(Sector::SIZE, 0, 0)));
    ASSERT_EQ(&follower.getTrack(), &scenery.getTrack("track2"));

    follower.move(follower.getPath().length());
    ASSERT_EQ(&follower.getSector(), &scenery.getSector(osg::Vec3(Sector::SIZE, Sector::SIZE, 0)));
    ASSERT_EQ(&follower.getTrack(), &scenery.getTrack("track3"));

    follower.move(follower.getPath().length());
    ASSERT_EQ(&follower.getSector(), &scenery.getSector(osg::Vec3(0, 0, 0)));
    ASSERT_EQ(&follower.getTrack(), &scenery.getTrack("track1"));
};

TEST_F(FollowerTest, moveBackward)
{
    Follower follower(scenery.getTrack("track1"), 0.1f);

    follower.move(-follower.getPath().length());
    ASSERT_EQ(&follower.getSector(), &scenery.getSector(osg::Vec3(Sector::SIZE, Sector::SIZE, 0)));
    ASSERT_EQ(&follower.getTrack(), &scenery.getTrack("track3"));

    follower.move(-follower.getPath().length());
    ASSERT_EQ(&follower.getSector(), &scenery.getSector(osg::Vec3(Sector::SIZE, 0, 0)));
    ASSERT_EQ(&follower.getTrack(), &scenery.getTrack("track2"));

    follower.move(-follower.getPath().length());
    ASSERT_EQ(&follower.getSector(), &scenery.getSector(osg::Vec3(0, 0, 0)));
    ASSERT_EQ(&follower.getTrack(), &scenery.getTrack("track1"));
};

TEST_F(FollowerTest, getPosition)
{
    const Path& path = scenery.getTrack("track1").getDefaultPath();
    Follower follower(scenery.getTrack("track1")); 

    // Begining of track
    ASSERT_EQ(follower.getPosition(), path.front());

    // 1/2 of track
    follower.move(path.length() * 0.5);
    ASSERT_EQ(follower.getPosition(), path.front() * 0.5 + path.back() * 0.5);

    // 3/4 of track
    follower.move(path.length() * 0.25);
    ASSERT_EQ(follower.getPosition(), path.front() * 0.25 + path.back() * 0.75);

    // End of track
    follower.move(path.length() * 0.25);
    ASSERT_EQ(follower.getPosition(), path.back());
}; 

int main(int argc, char **argv) 
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
