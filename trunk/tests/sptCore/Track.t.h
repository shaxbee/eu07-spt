#include <cxxtest/TestSuite.h>

#include "sptCore/Track.h"

using namespace sptCore;

class TrackTestSuite: public CxxTest::TestSuite
{
    
public:
    TrackTestSuite():
        _begin(0.0f, 0.0f, 0.0f), _end(10.0f, 10.0f, 10.0f), _track(_begin, _end) { };

    void testGetExit()
    {
        
        TS_ASSERT_EQUALS(_track.getExit(_begin), _end);
        TS_ASSERT_EQUALS(_track.getExit(_end), _begin);
        
        TS_ASSERT_THROWS(_track.getExit(osg::Vec3f(0.0f, 0.0f, 1.0f)), RailTracking::UnknownEntryException);
        
    };
    
    void testGetPath()
    {
        
        TS_ASSERT_EQUALS(_track.getPath(_begin)->back(), _end);
        TS_ASSERT_EQUALS(_track.getPath(_end)->back(), _begin);
       
        TS_ASSERT_DIFFERS(_track.getPath(_begin), _track.getPath(_end));
        
        TS_ASSERT_THROWS(_track.getPath(osg::Vec3f(0.0f, 0.0f, 1.0f)), RailTracking::UnknownEntryException);
        
    };
    
//    void testReverse()
//    {
//        
//        TS_ASSERT_EQUALS(_track.getPath(_begin), _track.reverse(_track.getPath(_end)));
//        TS_ASSERT_DIFFERS(_track.getPath(_begin), _track.reverse(_track.getPath(_begin)));
//        
//    };

private:
    osg::Vec3 _begin;
    osg::Vec3 _end;
    Track _track;
    
}; // TrackTestSuite
