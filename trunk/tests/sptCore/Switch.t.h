#include <cxxtest/TestSuite.h>

#include <sptCore/Switch.h>

#include <sptCore/DynamicScenery.h>
#include <sptCore/DynamicSector.h>

using namespace sptCore;

class SwitchTestSuite: public CxxTest::TestSuite
{
    
public:
    SwitchTestSuite():
        _begin(0.0f, 0.0f, 0.0f), 
        _straight(10.0f, 0.0f, 0.0f), 
        _diverted(10.0f, 10.0f, 0.0f), 
        _scenery(),
        _sector(_scenery, osg::Vec3()),
        _switch(_sector, _begin, _begin, _straight, _straight, _diverted, _diverted) 
    { 

    };
    
    void setUp()
    {
       
        _switch.setPosition("STRAIGHT");
        
    };

    void testSetPosition()
    {

        _switch.setPosition("STRAIGHT");
        TS_ASSERT_EQUALS(_switch.getPosition(), "STRAIGHT");

        _switch.setPosition("DIVERTED");
        TS_ASSERT_EQUALS(_switch.getPosition(), "DIVERTED");

        TS_ASSERT_THROWS(_switch.setPosition("INVALID"), Switch::InvalidPositionException);

    };

    void testGetExit()
    {
        
        _switch.setPosition("STRAIGHT");        
        
        TS_ASSERT_EQUALS(_switch.getExit(_begin), _straight);
        TS_ASSERT_EQUALS(_switch.getExit(_straight), _begin);
        
        TS_ASSERT_EQUALS(_switch.getExit(_diverted), _begin);
        
        TS_ASSERT_THROWS(_switch.getExit(osg::Vec3f(0.0f, 0.0f, 1.0f)), RailTracking::UnknownEntryException);        
        
        _switch.setPosition("DIVERTED");
        
        TS_ASSERT_EQUALS(_switch.getExit(_begin), _diverted);
        TS_ASSERT_EQUALS(_switch.getExit(_straight), _begin);
        
        TS_ASSERT_EQUALS(_switch.getExit(_diverted), _begin);
        
        TS_ASSERT_THROWS(_switch.getExit(osg::Vec3f(0.0f, 0.0f, 1.0f)), RailTracking::UnknownEntryException);
        
    };
    
    void testGetPath()
    {
        
        _switch.setPosition("STRAIGHT");

        // _begin -> _straight        
        TS_ASSERT_EQUALS(_switch.getPath(_begin).back(), _straight);
        // _diverted -> _begin
        TS_ASSERT_EQUALS(_switch.getPath(_diverted).back(), _begin);
        // _straight -> _begin
        TS_ASSERT_EQUALS(_switch.getPath(_straight).back(), _begin);
        // _diverted != _straight        
        TS_ASSERT_DIFFERS(_switch.getPath(_diverted).front(), _switch.getPath(_straight).front());

        // incorrect entry point
        TS_ASSERT_THROWS(_switch.getPath(osg::Vec3f(0.0f, 0.0f, 1.0f)), RailTracking::UnknownEntryException);
        
        _switch.setPosition("DIVERTED");        
        
        // _begin -> _diverted
        TS_ASSERT_EQUALS(_switch.getPath(_begin).back(), _diverted);
        // _diverted -> _begin
        TS_ASSERT_EQUALS(_switch.getPath(_diverted).back(), _begin);
        // _straight -> _begin
        TS_ASSERT_EQUALS(_switch.getPath(_straight).back(), _begin);
        // _diverted != _straight
        TS_ASSERT_DIFFERS(_switch.getPath(_diverted).front(), _switch.getPath(_straight).front());
                
        // incorrect entry point
        TS_ASSERT_THROWS(_switch.getPath(osg::Vec3f(0.0f, 0.0f, 1.0f)), RailTracking::UnknownEntryException);
       
    };
   
private:
    DynamicScenery _scenery;
    DynamicSector _sector;

    osg::Vec3 _begin;
    osg::Vec3 _straight;
    osg::Vec3 _diverted;
    Switch _switch;
    
}; // TrackTestSuite
