#ifndef SPTCORE_PATH_H
#define SPTCORE_PATH_H 1

#include <osg/Array>

namespace sptCore
{

class Path: public osg::Vec3Array
{

public:
    Path(osg::Vec3 front, osg::Vec3 back);
    Path(osg::Vec3 front, osg::Vec3 frontCP, osg::Vec3 back, osg::Vec3 backCP, int steps, float frontRoll = 0.0f, float backRoll = 0.0f);

    Path* reverse() const;

    osg::Vec3 getFrontCP() const { return _frontCP; }
    osg::Vec3 getBackCP() const { return _backCP; }

    float getFrontRoll() const { return _frontRoll; }
    float getBackRoll() const { return _backRoll; }

    typedef std::pair<osg::ref_ptr<Path>, osg::ref_ptr<Path> > Pair;

    static Pair straight(osg::Vec3 front, osg::Vec3 back);
    static Pair bezier(osg::Vec3 front, osg::Vec3 frontCP, osg::Vec3 back, osg::Vec3 backCP, int steps);

private:
    Path(): osg::Vec3Array() { }

    osg::Vec3 _frontCP;
    osg::Vec3 _backCP;

    float _frontRoll;
    float _backRoll;

}; // class sptCore::Path

} // namespace sptCore

#endif // headerguard
