#include <cxxtest/TestSuite.h>

#include "sptCore/Switch.h"

using namespace sptCore;

class SwitchTestSuite: public CxxTest::TestSuite
{
    
public:
    SwitchTestSuite():
        _begin(0.0f, 0.0f, 0.0f), 
        _straight(10.0f, 0.0f, 0.0f), 
        _diverted(10.0f, 10.0f, 0.0f), 
        _switch(_begin, _begin, _straight, _straight, _diverted, _diverted) { };
    
    void setUp()
    {
        
        _switch.setPosition(Switch::STRAIGHT);
        
    };
        
    void testGetExit()
    {
        
        _switch.setPosition(Switch::STRAIGHT);        
        
        TS_ASSERT_EQUALS(_switch.getExit(_begin), _straight);
        TS_ASSERT_EQUALS(_switch.getExit(_straight), _begin);
        
        TS_ASSERT_EQUALS(_switch.getExit(_diverted), _begin);
        
        TS_ASSERT_THROWS(_switch.getExit(osg::Vec3f(0.0f, 0.0f, 1.0f)), RailTracking::UnknownEntryException);        
        
        _switch.setPosition(Switch::DIVERTED);
        
        TS_ASSERT_EQUALS(_switch.getExit(_begin), _diverted);
        TS_ASSERT_EQUALS(_switch.getExit(_straight), _begin);
        
        TS_ASSERT_EQUALS(_switch.getExit(_diverted), _begin);
        
        TS_ASSERT_THROWS(_switch.getExit(osg::Vec3f(0.0f, 0.0f, 1.0f)), RailTracking::UnknownEntryException);
        
    };
    
    void testGetPath()
    {
        
        _switch.setPosition(Switch::STRAIGHT);

        // _begin -> _straight        
        TS_ASSERT_EQUALS(_switch.getPath(_begin)->front(), _straight);
        // _diverted -> _begin
        TS_ASSERT_EQUALS(_switch.getPath(_diverted)->front(), _begin);
        // _straight -> _begin
        TS_ASSERT_EQUALS(_switch.getPath(_straight)->front(), _begin);
        // _diverted != _straight        
        TS_ASSERT_DIFFERS(_switch.getPath(_diverted)->front(), _switch.getPath(_straight)->front());

        // incorrect entry point
        TS_ASSERT_THROWS(_switch.getPath(osg::Vec3f(0.0f, 0.0f, 1.0f)), RailTracking::UnknownEntryException);
        
        _switch.setPosition(Switch::DIVERTED);        
        
        // _begin -> _diverted
        TS_ASSERT_EQUALS(_switch.getPath(_begin)->front(), _diverted);
        // _diverted -> _begin
        TS_ASSERT_EQUALS(_switch.getPath(_diverted)->front(), _begin);
        // _straight -> _begin
        TS_ASSERT_EQUALS(_switch.getPath(_straight)->front(), _begin);
        // _diverted != _straight
        TS_ASSERT_DIFFERS(_switch.getPath(_diverted)->front(), _switch.getPath(_straight)->front());
                
        // incorrect entry point
        TS_ASSERT_THROWS(_switch.getPath(osg::Vec3f(0.0f, 0.0f, 1.0f)), RailTracking::UnknownEntryException);
       
    };
    
    void testReverse()
    {
        
        _switch.setPosition(Switch::STRAIGHT);        
        
        // _begin, _straight -> _straight, _begin
        TS_ASSERT_EQUALS(_switch.getPath(_begin), _switch.reverse(_switch.getPath(_straight)));
        // _begin, _straight != _begin -> _straight
        TS_ASSERT_DIFFERS(_switch.getPath(_begin), _switch.reverse(_switch.getPath(_begin)));
        // _diverted, _begin != _straight -> _begin
        TS_ASSERT_DIFFERS(_switch.getPath(_diverted), _switch.reverse(_switch.getPath(_begin)));
        
    };

private:
    osg::Vec3 _begin;
    osg::Vec3 _straight;
    osg::Vec3 _diverted;
    Switch _switch;
    
}; // TrackTestSuite
