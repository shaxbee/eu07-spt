#include <gtest/gtest.h>

#include <osg/io_utils>

#include <sptCore/Switch.h>
#include <sptCore/Sector.h>

using namespace sptCore;

class SwitchTest: public ::testing::Test
{
    
public:
    SwitchTest():
        sector(osg::Vec3()),
        begin(0.0f, 0.0f, 0.0f), 
        straight(10.0f, 0.0f, 0.0f), 
        diverted(10.0f, 10.0f, 0.0f), 
        switch_(sector, new StraightPath(begin, straight), new StraightPath(begin, diverted), "STRAIGHT") 
    { 
    };

protected:
    Sector sector;

    osg::Vec3 begin;
    osg::Vec3 straight;
    osg::Vec3 diverted;
    Switch switch_;
    
}; // SwitchTest

TEST_F(SwitchTest, SetPosition)
{
    switch_.setPosition("STRAIGHT");
    ASSERT_EQ(switch_.getPosition(), "STRAIGHT");

    switch_.setPosition("DIVERTED");
    ASSERT_EQ(switch_.getPosition(), "DIVERTED");

    ASSERT_THROW(switch_.setPosition("INVALID"), Switch::InvalidPositionException);
};

TEST_F(SwitchTest, GetExit)
{
    switch_.setPosition("STRAIGHT");        
    
    ASSERT_EQ(switch_.getExit(begin), straight);
    ASSERT_EQ(switch_.getExit(straight), begin);    
    ASSERT_EQ(switch_.getExit(diverted), begin);
    
    ASSERT_THROW(switch_.getExit(osg::Vec3f(0.0f, 0.0f, 1.0f)), RailTracking::UnknownEntryException);        
    
    switch_.setPosition("DIVERTED");
    
    ASSERT_EQ(switch_.getExit(begin), diverted);
    ASSERT_EQ(switch_.getExit(straight), begin);
    ASSERT_EQ(switch_.getExit(diverted), begin);
    
    ASSERT_THROW(switch_.getExit(osg::Vec3f(0.0f, 0.0f, 1.0f)), RailTracking::UnknownEntryException);    
};
  
TEST_F(SwitchTest, GetPath)
{
    switch_.setPosition("STRAIGHT");

    // begin -> straight        
    ASSERT_EQ(switch_.getPath(begin).back(), straight);
    // diverted -> begin
    ASSERT_EQ(switch_.getPath(diverted).back(), begin);
    // straight -> begin
    ASSERT_EQ(switch_.getPath(straight).back(), begin);
    // diverted != straight        
    ASSERT_NE(switch_.getPath(diverted).front(), switch_.getPath(straight).front());

    // incorrect entry point
    ASSERT_THROW(switch_.getPath(osg::Vec3f(0.0f, 0.0f, 1.0f)), RailTracking::UnknownEntryException);
    
    switch_.setPosition("DIVERTED");        
    
    // begin -> diverted
    ASSERT_EQ(switch_.getPath(begin).back(), diverted);
    // diverted -> begin
    ASSERT_EQ(switch_.getPath(diverted).back(), begin);
    // straight -> begin
    ASSERT_EQ(switch_.getPath(straight).back(), begin);
    // diverted != straight
    ASSERT_NE(switch_.getPath(diverted).front(), switch_.getPath(straight).front());
            
    // incorrect entry point
    ASSERT_THROW(switch_.getPath(osg::Vec3f(0.0f, 0.0f, 1.0f)), RailTracking::UnknownEntryException);
};