#include <cxxtest/TestSuite.h>

#include <boost/shared_ptr.hpp>

#include <sptCore/DynamicSector.h>
#include <sptCore/Track.h>

using namespace sptCore;

class DynamicSectorTestSuite: public CxxTest::TestSuite
{

public:
    DynamicSectorTestSuite(): 
        _sector(osg::Vec3(0, 0, 0)),
        _pointA(0, 0, 0),
        _pointB(100, 0, 0),
        _pointC(200, 0, 0),
        _trackA(new Track(_pointA, _pointB)),
        _trackB(new Track(_pointB, _pointC))
    { 
    
    };

    void setUp()
    {

        _sector = DynamicSector(osg::Vec3(0, 0, 0));

    }

    void testGetNextTrack()
    {

        _sector.addTrack(_trackA.get(), _pointA);
        _sector.addConnection(_trackA.get(), _trackB.get(), _pointB);
        _sector.addTrack(_trackB.get(), _pointC);

        TS_ASSERT_EQUALS(_sector.getNextTrack(_pointA, _trackA.get()), (Track*) NULL);
        TS_ASSERT_EQUALS(_sector.getNextTrack(_pointB, _trackA.get()), _trackB.get());
        TS_ASSERT_EQUALS(_sector.getNextTrack(_pointB, _trackB.get()), _trackA.get());
        TS_ASSERT_EQUALS(_sector.getNextTrack(_pointC, _trackB.get()), (Track*) NULL);
        TS_ASSERT_THROWS(_sector.getNextTrack(osg::Vec3(17, 17, 17), _trackA.get()), Sector::UnknownConnectionException);

    };

    void testGetConnection()
    {

        _sector.addTrack(_trackA.get(), _pointA);
        _sector.addConnection(_trackA.get(), _trackB.get(), _pointB);
        _sector.addTrack(_trackB.get(), _pointC);

        TS_ASSERT_EQUALS(_sector.getConnection(_pointA), Sector::Connection(_trackA.get(), NULL));
        TS_ASSERT_EQUALS(_sector.getConnection(_pointB), Sector::Connection(_trackA.get(), _trackB.get()));
        TS_ASSERT_EQUALS(_sector.getConnection(_pointC), Sector::Connection(_trackB.get(), NULL));
        TS_ASSERT_THROWS(_sector.getConnection(osg::Vec3(17, 17, 17)), Sector::UnknownConnectionException);

    };

private:
    DynamicSector _sector;

    osg::Vec3 _pointA;
    osg::Vec3 _pointB;
    osg::Vec3 _pointC;

    boost::shared_ptr<Track> _trackA;
    boost::shared_ptr<Track> _trackB;

}; // DynamicSectorTestSuite 
