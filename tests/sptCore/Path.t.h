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

        StraightPath path(begin, end);

        TS_ASSERT_EQUALS(path.front(), begin);
        TS_ASSERT_EQUALS(path.back(), end);

        TS_ASSERT_EQUALS(path.points()->getNumElements(), 2);

    };

    void testBezier()
    {

        osg::Vec3 begin(0.0f, 0.0f, 0.0f);
        osg::Vec3 end(100.0f, 100.0f, 10.0f);

        BezierPath path(begin, osg::Vec3(100.0f, 0.0f, 10.0f), end, osg::Vec3(0.0f, 100.0f, 0.0f));

        TS_ASSERT_EQUALS(path.front(), begin);
        TS_ASSERT_EQUALS(path.back(), end);
//        TS_ASSERT_EQUALS(path.points()->getNumElements(), 33);

    };

};
