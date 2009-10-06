#include <cxxtest/TestSuite.h>
#include <sptCore/DynamicScenery.h>

#include <boost/scoped_ptr.hpp>

#include <sptCore/Track.h>
#include <sptCore/Switch.h>
#include <sptCore/DynamicSector.h>

using namespace sptCore;

class DynamicSceneryTestSuite: public CxxTest::TestSuite
{
public:
    DynamicSceneryTestSuite() { };

    void setUp()
    {

        _scenery.reset(new DynamicScenery());
        _scenery->addSector(std::auto_ptr<Sector>(new DynamicSector(*_scenery, osg::Vec3())));

    };

    void testTrack()
    {

        DynamicSector& sector = dynamic_cast<DynamicSector&>(_scenery->getSector(osg::Vec3()));
        
        osg::Vec3 dummy(0, 0, 0);
        Track* testTrack = new Track(sector, dummy, dummy);
    
        _scenery->addTrack("track1", *testTrack);
        sector.addTrack(std::auto_ptr<RailTracking>(testTrack));
        
        TS_ASSERT_EQUALS(&_scenery->getTrack("track1"), testTrack);
        TS_ASSERT_THROWS(&_scenery->getTrack("track2"), Scenery::RailTrackingNotFoundException);
        
    };

    void testSwitch()
    {

        DynamicSector& sector = dynamic_cast<DynamicSector&>(_scenery->getSector(osg::Vec3()));
        
        osg::Vec3 dummy(0, 0, 0);
        Switch* testSwitch = new Switch(sector, dummy, dummy, dummy, dummy, dummy, dummy);

        _scenery->addSwitch("switch1", *testSwitch);
        sector.addTrack(std::auto_ptr<RailTracking>(testSwitch));
        
        TS_ASSERT_EQUALS(&_scenery->getSwitch("switch1"), testSwitch);
        TS_ASSERT_THROWS(&_scenery->getSwitch("switch2"), Scenery::RailTrackingNotFoundException);
        
    };

    void testSector()
    {

        TS_ASSERT(_scenery->hasSector(osg::Vec3()));

    };
    
private:
    boost::scoped_ptr<DynamicScenery> _scenery;
    DynamicSector* _sector;
    
}; // class DynamicSceneryTestSuite
