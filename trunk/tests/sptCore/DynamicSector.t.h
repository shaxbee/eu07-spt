#include <cxxtest/TestSuite.h>

#include <boost/scoped_ptr.hpp>

#include <sptCore/DynamicScenery.h>
#include <sptCore/DynamicSector.h>
#include <sptCore/Track.h>

using namespace sptCore;

class DynamicSectorTestSuite: public CxxTest::TestSuite
{

public:
    DynamicSectorTestSuite(): 
        _pointA(0, 0, 0),
        _pointB(100, 0, 0),
        _pointC(200, 0, 0)
    { 
    
    };

    void setUp()
    {

		_sector.reset(new DynamicSector(_scenery, osg::Vec3(0, 0, 0)));
		
		std::auto_ptr<Track> trackA(new Track(*_sector, _pointA, _pointB));
        std::auto_ptr<Track> trackB(new Track(*_sector, _pointB, _pointC));

		_trackA = trackA.get();
		_trackB = trackB.get();

		_sector->addTrack(std::auto_ptr<RailTracking>(trackA));
		_sector->addTrack(std::auto_ptr<RailTracking>(trackB));

        _sector->addConnection(_pointA, _trackA);
        _sector->addConnection(_pointB, _trackA, _trackB);
        _sector->addConnection(_pointC, _trackB);

    }

    void testGetNextTrack()
    {

        TS_ASSERT_EQUALS(&_sector->getNextTrack(_pointA, _trackA), (Track*) NULL);
        TS_ASSERT_EQUALS(&_sector->getNextTrack(_pointB, _trackA), _trackB);
        TS_ASSERT_EQUALS(&_sector->getNextTrack(_pointB, _trackB), _trackA);
        TS_ASSERT_EQUALS(&_sector->getNextTrack(_pointC, _trackB), (Track*) NULL);
        TS_ASSERT_THROWS(_sector->getNextTrack(osg::Vec3(17, 17, 17), _trackA), Sector::UnknownConnectionException);

    };

    void testGetConnection()
    {

        TS_ASSERT_EQUALS(_sector->getConnection(_pointA), Sector::Connection(_trackA, NULL));
        TS_ASSERT_EQUALS(_sector->getConnection(_pointB), Sector::Connection(_trackA, _trackB));
        TS_ASSERT_EQUALS(_sector->getConnection(_pointC), Sector::Connection(_trackB, NULL));
        TS_ASSERT_THROWS(_sector->getConnection(osg::Vec3(17, 17, 17)), Sector::UnknownConnectionException);

    };

private:
	DynamicScenery _scenery;
	std::auto_ptr<DynamicSector> _sector;

    osg::Vec3 _pointA;
    osg::Vec3 _pointB;
    osg::Vec3 _pointC;

    Track* _trackA;
    Track* _trackB;

}; // DynamicSectorTestSuite 
