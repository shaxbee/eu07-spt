#include <cxxtest/TestSuite.h>

#include <boost/array.hpp>

#include <sptCore/Track.h>
#include <sptCore/Sector.h>

namespace sptCore
{
    struct Scenery { };
}

using namespace sptCore;

class SectorTestSuite: public CxxTest::TestSuite
{

public:
    SectorTestSuite(): 
        _pointA(0, 0, 0),
        _pointB(100, 0, 0),
        _pointC(200, 0, 0)
    { 
    };

    void setUp()
    {
        _sector.reset(new Sector(_pointA));

        std::auto_ptr<Path> path1(new StraightPath(_pointA, _pointB));
        std::auto_ptr<Path> path2(new StraightPath(_pointB, _pointC));

        boost::array<RailTracking*, 2> tracks =
        {{
            new Track(*_sector, path1),
            new Track(*_sector, path2)
        }};

        boost::array<Sector::Connection, 2> connections =
        {{
            {_pointA, NULL, tracks[0]},
            {_pointB, tracks[0], tracks[1]}
        }};

        _sector->setData(tracks, connections);
    }

    void testGetNextTrack()
    {
        TS_ASSERT_THROWS(_sector->getNextTrack(_pointA, _sector->getRailTracking(0)), Sector::UnknownConnectionException);
        TS_ASSERT_THROWS(_sector->getNextTrack(_pointC, _sector->getRailTracking(0)), Sector::UnknownConnectionException);
        TS_ASSERT_THROWS(_sector->getNextTrack(osg::Vec3(17, 17, 17), _sector->getRailTracking(0)), Sector::UnknownConnectionException);

        TS_ASSERT_EQUALS(&_sector->getNextTrack(_pointB, _sector->getRailTracking(0)), &_sector->getRailTracking(1));
        TS_ASSERT_EQUALS(&_sector->getNextTrack(_pointB, _sector->getRailTracking(1)), &_sector->getRailTracking(0));
    };

    void testUpdateConnections()
    {
        boost::array<Sector::ConnectionUpdate, 1> updates =
        {
            {_pointA, NULL, &_sector->getRailTracking(1)}
        };

        _sector->updateConnections(updates);

        TS_ASSERT_EQUALS(&_sector->getNextTrack(_pointA, _sector->getRailTracking(0)), &_sector->getRailTracking(1));
    };


private:
    std::auto_ptr<Sector> _sector;

    const osg::Vec3 _pointA;
    const osg::Vec3 _pointB;
    const osg::Vec3 _pointC;

}; // DynamicSectorTestSuite 
