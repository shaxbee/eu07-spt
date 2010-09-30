#include <gtest/gtest.h>

#include <sptCore/Path.h>

using namespace sptCore;

TEST(PathTest, Straight)
{
    osg::Vec3 begin(0.0f, 0.0f, 0.0f);
    osg::Vec3 end(100.0f, 100.0f, 0.0f);

    StraightPath path(begin, end);

    ASSERT_EQ(path.front(), begin);
    ASSERT_EQ(path.back(), end);

    ASSERT_EQ(path.points()->getNumElements(), 2);
};

TEST(PathTest, Bezier)
{
    osg::Vec3 begin(0.0f, 0.0f, 0.0f);
    osg::Vec3 end(100.0f, 100.0f, 10.0f);

    BezierPath path(begin, osg::Vec3(100.0f, 0.0f, 10.0f), end, osg::Vec3(100.0f, 0.0f, 0.0f));

    ASSERT_EQS(path.front(), begin);
    ASSERT_EQS(path.back(), end);
    ASSERT_NEAR(path.length(), 114.0f, 0.5f);

    ASSERT_NEAR(path.frontDir().x(), 1.0f, 0.01f);
    ASSERT_NEAR(path.backDir().y(), 1.0f, 0.01f);
};
