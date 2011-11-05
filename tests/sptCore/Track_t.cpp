#include <gtest/gtest.h>

#include <osg/io_utils>

#include <sptCore/Track.h>
#include <sptCore/Sector.h>

using namespace sptCore;

class TrackTest: public ::testing::Test
{
public:
    TrackTest():
        begin(0.0f, 0.0f, 0.0f), 
        end(10.0f, 10.0f, 10.0f), 
        sector(osg::Vec3()),
        track(sector, new StraightPath(begin, end)) 
    { 
    };
        
protected:
    osg::Vec3 begin;
    osg::Vec3 end;

    Sector sector;
    Track track;    
}; // TrackTest

TEST_F(TrackTest, GetExit)
{        
    ASSERT_EQ(track.getExit(begin), end);
    ASSERT_EQ(track.getExit(end), begin);
    
    ASSERT_THROW(track.getExit(osg::Vec3f(0.0f, 0.0f, 1.0f)), RailTracking::UnknownEntryException);
};
    
TEST_F(TrackTest, GetPath)
{
    ASSERT_EQ(track.getPath(begin)->back(), end);
    ASSERT_EQ(track.getPath(end)->back(), begin);
   
//    ASSERT_NE(track.getPath(begin), track.getPath(end));
    
    ASSERT_THROW(track.getPath(osg::Vec3f(0.0f, 0.0f, 1.0f)), RailTracking::UnknownEntryException);
};