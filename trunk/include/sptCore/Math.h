#ifndef SPTCORE_MATH_H
#define SPTCORE_MATH_H 1

#include <osg/Vec3>
#include <osg/Matrix>

namespace sptCore
{

osg::Matrix rotationMatrix(osg::Vec3 dir, float roll = 0.0f)
{

    osg::Matrix result;
    dir.normalize();

    osg::Vec3 refX;

    if(dir.x() == 0.0f && dir.z() == 0.0f)
    {
        refX = osg::Vec3(-dir.y(), 0.0f, 0.0f);
    }
    else
    {
        refX = osg::Vec3(0.0f, 1.0f, 0.0f);
    };

    osg::Vec3 refZ = refX ^ dir;
    refZ.normalize();

    refX = -(refZ ^ dir);
    refX.normalize();

    result.set(
        refX.x(), refX.y(), refX.z(), 0.0f,
        dir.x(),  dir.y(),  dir.z(),  0.0f,
        refZ.x(), refZ.y(), refZ.z(), 0.0f,
        0.0f,     0.0f,     0.0f,     1.0f
    );

    return result;
//    return osg::Matrix::inverse(result);

}; // sptCore::rotationMatrix

inline osg::Vec3 mix(const osg::Vec3& left, const osg::Vec3& right, float ratio)
{

    return (left * ratio) + (right * (1 - ratio));

}; // sptCore::mix

}; // namespace sptCore

#endif // header guard
