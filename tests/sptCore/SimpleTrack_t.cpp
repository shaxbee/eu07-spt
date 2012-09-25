#include <gtest/gtest.h>

#include <osg/io_utils>

#include <sptCore/SimpleTrack.h>
#include <sptCore/Sector.h>

using namespace sptCore;

class SimpleTrackTest: public ::testing::Test
{
public:
    SimpleTrackTest():
        begin(0.0f, 0.0f, 0.0f), 
        end(10.0f, 10.0f, 10.0f), 
        track(osg::Vec2f(), std::make_shared<StraightPath>(begin, end), TrackId::null(), TrackId::null()) 
    { 
    };
        
protected:
    osg::Vec3 sector;
    osg::Vec3 begin;
    osg::Vec3 end;

    SimpleTrack track;    
}; // SimpleTrackTest

TEST_F(SimpleTrackTest, GetExit)
{        
    ASSERT_EQ(track.getExit(begin), end);
    ASSERT_EQ(track.getExit(end), begin);
    
    ASSERT_THROW(track.getExit(osg::Vec3f(0.0f, 0.0f, 1.0f)), SimpleTrack::UnknownEntryException);
};
    
TEST_F(SimpleTrackTest, GetPath)
{
    ASSERT_EQ(track.getPath(begin)->back(), end);
    ASSERT_EQ(track.getPath(end)->back(), begin);
   
//    ASSERT_NE(track.getPath(begin), track.getPath(end));
    
    ASSERT_THROW(track.getPath(osg::Vec3f(0.0f, 0.0f, 1.0f)), SimpleTrack::UnknownEntryException);
};
