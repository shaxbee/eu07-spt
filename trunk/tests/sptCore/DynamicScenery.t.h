#include <cxxtest/TestSuite.h>
#include <sptCore/DynamicScenery.h>

using namespace sptCore;

class DynamicSceneryTestSuite: public CxxTest::TestSuite
{
public:
	void setUp()
	{
		_scenery = DynamicScenery();
	};
	
	void testTrack()
	{
		
		osg::Vec3 dummy(0, 0, 0)
		boost::shared_ptr<Track> testTrack(new Track(dummy, dummy));
		
		scenery.addTrack("track1", testTrack.get());
		
		TS_ASSERT_EQUALS(_scenery.getTrack("track1"), testTrack.get());
		TS_ASSERT_THROWS(_scenery.getTrack("track2"), UnknownRailTrackingException);
		
	};

	void testSwitch()
	{
		
		osg::Vec3 dummy(0, 0, 0);
		boost::shared_ptr<Switch> testSwitch(new Switch(dummy, dummy, dummy, dummy, dummy, dummy));
		
		scenery.addSwitch("switch1", testSwitch.get());
		
		TS_ASSERT_EQUALS(_scenery.getSwitch("switch1"), testSwitch.get());
		TS_ASSERT_THROWS(_scenery.getSwitch("switch2"), UnknownRailTrackingException);
		
	};
	
//	void testEventedTrack()
//	{
//		
//	};
	
private:
	DynamicScenery _scenery;
	
}; // class DynamicSceneryTestSuite