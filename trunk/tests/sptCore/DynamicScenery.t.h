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
        _sector = new DynamicSector(*_scenery, osg::Vec3());

        _scenery->addSector(_sector);

    };

	void testTrack()
	{
		
		osg::Vec3 dummy(0, 0, 0);
        Track* testTrack = new Track(*_sector, dummy, dummy);
	
        _sector->addTrack(testTrack);    
		_scenery->addTrack("track1", testTrack);
		
		TS_ASSERT_EQUALS(&_scenery->getTrack("track1"), testTrack);
		TS_ASSERT_THROWS(&_scenery->getTrack("track2"), Scenery::UnknownRailTrackingException);
		
	};

	void testSwitch()
	{
		
		osg::Vec3 dummy(0, 0, 0);
		Switch* testSwitch = new Switch(*_sector, dummy, dummy, dummy, dummy, dummy, dummy);
	
        _sector->addTrack(testSwitch);    
		_scenery->addSwitch("switch1", testSwitch);
		
		TS_ASSERT_EQUALS(&_scenery->getSwitch("switch1"), testSwitch);
		TS_ASSERT_THROWS(&_scenery->getSwitch("switch2"), Scenery::UnknownRailTrackingException);
		
	};

    void testSector()
    {

        TS_ASSERT(_scenery->hasSector(osg::Vec3()));

    };
	
private:
    boost::scoped_ptr<DynamicScenery> _scenery;
    DynamicSector* _sector;
	
}; // class DynamicSceneryTestSuite
