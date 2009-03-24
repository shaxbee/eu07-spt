#include <cxxtest/TestSuite.h>

#include "sptCore/Path.h"

using namespace sptCore;

class PathTestSuite: public CxxTest::TestSuite
{

public:
    void testStraight()
    {

        osg::Vec3 begin(0.0f, 0.0f, 0.0f);
        osg::Vec3 end(100.0f, 100.0f, 0.0f);

        Path::Pair path = Path::straight(begin, end);

        TS_ASSERT_EQUALS(path.first->front(), begin);
        TS_ASSERT_EQUALS(path.second->back(), begin);

        TS_ASSERT_EQUALS(path.first->back(), end);
        TS_ASSERT_EQUALS(path.second->front(), end);

        TS_ASSERT_EQUALS(path.first->getNumElements(), 2);
        TS_ASSERT_EQUALS(path.second->getNumElements(), 2);

    };

    void testBezier()
    {

        osg::Vec3 begin(0.0f, 0.0f, 0.0f);
        osg::Vec3 end(100.0f, 100.0f, 10.0f);

        Path::Pair path = Path::bezier(begin, osg::Vec3(100.0f, 0.0f, 10.0f), end, osg::Vec3(0.0f, 100.0f, 0.0f), 32);

        TS_ASSERT_EQUALS(path.first->front(), begin);
        TS_ASSERT_EQUALS(path.second->back(), begin);

        TS_ASSERT_EQUALS(path.first->back(), end);
        TS_ASSERT_EQUALS(path.second->front(), end);

        TS_ASSERT_EQUALS(path.first->getNumElements(), 33);
        TS_ASSERT_EQUALS(path.second->getNumElements(), 33);
    };

};
