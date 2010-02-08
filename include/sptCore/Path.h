#ifndef SPTCORE_PATH_H
#define SPTCORE_PATH_H 1

#include <osg/Array>

namespace sptCore
{

//! \brief Path between two 3D points
//! Path is vector of osg::Vec3 points that could form straight line or bezier curve
//! \author Zbyszek "ShaXbee" Mandziejewicz
class Path : public osg::Vec3Array
{

public:
    Path(osg::Vec3 front, osg::Vec3 back);
    Path(osg::Vec3 front, osg::Vec3 frontCP, osg::Vec3 back, osg::Vec3 backCP, int steps, float frontRoll = 0.0f, float backRoll = 0.0f);

//    static Path* reverse(const Path* source);

    //! Return reversed path
    Path* reverse() const;

    float length() const { return _length; }

    //! Return normalized front direction vector
    const osg::Vec3& frontDir() const { return _frontDir; }
    //! Return normalized back direction vector
    const osg::Vec3& backDir() const { return _backDir; }

    float frontRoll() const { return _frontRoll; }
    float backRoll() const { return _backRoll; }

private:
    Path() : osg::Vec3Array() { }

    osg::Vec3 _frontDir;
    osg::Vec3 _backDir;

    float _length;
    float _frontRoll;
    float _backRoll;

}; // class sptCore::Path

} // namespace sptCore

#endif // headerguard
