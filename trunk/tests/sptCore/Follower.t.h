#include <cxxtest/TestSuite.h>

#include <boost/scoped_ptr.hpp>

#include <sptCore/Follower.h>

#include <sptCore/DynamicScenery.h>
#include <sptCore/DynamicSector.h>
#include <sptCore/Track.h>

using namespace sptCore;

class FollowerTestSuite: public CxxTest::TestSuite
{

public:
    void setUp()
    {

        _scenery.reset(new DynamicScenery());

        _sectorA = new DynamicSector(_scenery.get(), osg::Vec3(0, 0, 0));
        _sectorB = new DynamicSector(_scenery.get(), osg::Vec3(Sector::SIZE, 0, 0));
        _sectorC = new DynamicSector(_scenery.get(), osg::Vec3(Sector::SIZE, 0, Sector::SIZE));

        _scenery->addSector(_sectorA);
        _scenery->addSector(_sectorB);
        _scenery->addSector(_sectorC);

        osg::Vec3 point1(Sector::SIZE / 2, 0, Sector::SIZE /2);
        osg::Vec3 point2(Sector::SIZE * 1.5, 0, Sector::SIZE / 2);
        osg::Vec3 point3(Sector::SIZE / 2, 0, Sector::SIZE * 1.5);
        osg::Vec3 point4(-Sector::SIZE / 2, 0, -Sector::SIZE / 2);

        _trackA = new Track(point1, point2);
        _trackB = new Track(point1, point3);
        _trackC = new Track(point1, point4);

        _sectorA->addTrack(_trackA);
        _sectorB->addTrack(_trackB);
        _sectorC->addTrack(_trackC);

        _sectorB->addConnection(point1, _trackA, _trackB);
        _sectorC->addConnection(point1, _trackB, _trackC);
        _sectorA->addConnection(point1, _trackC, _trackA);

        _scenery->addTrack("startTrack", _trackA);

    };

	void testTrack()
	{

        boost::scoped_ptr<Follower> follower(new Follower(_sectorA, &_scenery->getTrack("startTrack"), 0.1f));

        float length = _trackA->getPath()->length();

        follower->move(length);
        TS_ASSERT_EQUALS(&follower->getSector(), _sectorB);
        TS_ASSERT_EQUALS(&follower->getTrack(), _trackB);
		
	};

private:
    boost::scoped_ptr<DynamicScenery> _scenery;

    DynamicSector* _sectorA;
    DynamicSector* _sectorB;
    DynamicSector* _sectorC;

    Track* _trackA;
    Track* _trackB;
    Track* _trackC;
    Track* _trackD;

	
}; // class FollowerTestSuite
