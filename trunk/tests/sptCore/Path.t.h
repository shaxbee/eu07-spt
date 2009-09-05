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

        Path path(begin, end);

        TS_ASSERT_EQUALS(path.front(), begin);
        TS_ASSERT_EQUALS(path.back(), end);

        TS_ASSERT_EQUALS(path.getNumElements(), 2);

    };

    void testBezier()
    {

        osg::Vec3 begin(0.0f, 0.0f, 0.0f);
        osg::Vec3 end(100.0f, 100.0f, 10.0f);

        Path path(begin, osg::Vec3(100.0f, 0.0f, 10.0f), end, osg::Vec3(0.0f, 100.0f, 0.0f), 32);

        TS_ASSERT_EQUALS(path.front(), begin);
        TS_ASSERT_EQUALS(path.back(), end);
        TS_ASSERT_EQUALS(path.getNumElements(), 33);

    };

};
