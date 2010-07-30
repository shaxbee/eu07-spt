#include <cxxtest/TestSuite.h>
#include <sptCore/Scenery.h>

#include <boost/scoped_ptr.hpp>

#include <sptCore/Track.h>
#include <sptCore/Switch.h>
#include <sptCore/Sector.h>

using namespace sptCore;

class SceneryTestSuite: public CxxTest::TestSuite
{
public:
    SceneryTestSuite() { };

    void setUp()
    {
        _scenery.reset(new Scenery());
    };

    void testTrack()
    {
        Sector sector(_dummy);
        
        std::auto_ptr<Track> testTrack(new Track(sector, new StraightPath(_dummy, _dummy)));
    
        _scenery->addTrack("track1", *testTrack);

        TS_ASSERT_EQUALS(&_scenery->getTrack("track1"), testTrack.get());
        TS_ASSERT_THROWS(&_scenery->getTrack("track2"), Scenery::RailTrackingNotFoundException);
    };

    void testSwitch()
    {
        Sector sector(_dummy);
        
        std::auto_ptr<Switch> testSwitch(new Switch(sector, new StraightPath(_dummy, _dummy), new StraightPath(_dummy, _dummy)));

        _scenery->addSwitch("switch1", *testSwitch);
        
        TS_ASSERT_EQUALS(&_scenery->getSwitch("switch1"), testSwitch.get());
        TS_ASSERT_THROWS(&_scenery->getSwitch("switch2"), Scenery::RailTrackingNotFoundException);
    };

    void testSector()
    {
        std::auto_ptr<Sector> sector(new Sector(_dummy));
        _scenery->addSector(sector);

        TS_ASSERT(_scenery->hasSector(_dummy));
    };
    
private:
    boost::scoped_ptr<Scenery> _scenery;
    osg::Vec3 _dummy;
    
}; // class SceneryTestSuite
