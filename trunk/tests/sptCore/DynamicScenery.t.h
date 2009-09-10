#include <cxxtest/TestSuite.h>
#include <sptCore/DynamicScenery.h>

#include <sptCore/Sector.h>
#include <sptCore/Track.h>
#include <sptCore/Switch.h>

using namespace sptCore;

class DynamicSceneryTestSuite: public CxxTest::TestSuite
{
public:
    DynamicSceneryTestSuite(): _scenery(new DynamicScenery()) { };

	void testTrack()
	{
		
		osg::Vec3 dummy(0, 0, 0);
		boost::shared_ptr<Track> testTrack(new Track(dummy, dummy));
		
		_scenery->addTrack("track1", testTrack.get());
		
		TS_ASSERT_EQUALS(_scenery->getTrack("track1"), testTrack.get());
		TS_ASSERT_THROWS(_scenery->getTrack("track2"), Scenery::UnknownRailTrackingException);
		
	};

	void testSwitch()
	{
		
		osg::Vec3 dummy(0, 0, 0);
		boost::shared_ptr<Switch> testSwitch(new Switch(dummy, dummy, dummy, dummy, dummy, dummy));
		
		_scenery->addSwitch("switch1", testSwitch.get());
		
		TS_ASSERT_EQUALS(_scenery->getSwitch("switch1"), testSwitch.get());
		TS_ASSERT_THROWS(_scenery->getSwitch("switch2"), Scenery::UnknownRailTrackingException);
		
	};
	
//	void testEventedTrack()
//	{
//		
//	};
	
private:
    boost::shared_ptr<DynamicScenery> _scenery;
	
}; // class DynamicSceneryTestSuite
