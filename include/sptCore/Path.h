#ifndef SPTCORE_PATH_H
#define SPTCORE_PATH_H 1

#include <limits>
#include <memory>
#include <vector>

#include <osg/Array>

namespace sptCore
{

//! \brief Path between two 3D points
//! Path is vector of osg::Vec3 points that could form straight line or bezier curve
//! \author Zbyszek "ShaXbee" Mandziejewicz
class Path
{

public:
    Path(const osg::Vec3f& front, const osg::Vec3f& back): _front(front), _back(back) { };
    virtual ~Path() { };

    virtual std::auto_ptr<Path> clone() const = 0;
    //! Return reversed path
    virtual std::auto_ptr<Path> reverse() const = 0;

    const osg::Vec3f& front() const { return _front; }
    const osg::Vec3f& back() const { return _back; }

    virtual osg::Vec3f frontDir() const = 0;
    virtual osg::Vec3f backDir() const = 0;

    virtual float length() const = 0;

    static const float DEFAULT_SCALE;

    virtual osg::ref_ptr<osg::Vec3Array> points(float scale = DEFAULT_SCALE) const = 0;

private:
    osg::Vec3 _front;
    osg::Vec3 _back;

}; // class sptCore::Path

class StraightPath: public Path
{
public:
    StraightPath(const osg::Vec3f& front, const osg::Vec3f& back): Path(front, back) { };
    virtual ~StraightPath();

    virtual std::auto_ptr<Path> clone() const;
    virtual std::auto_ptr<Path> reverse() const;

    virtual osg::Vec3f frontDir() const;
    virtual osg::Vec3f backDir() const;

    virtual float length() const;
    virtual osg::ref_ptr<osg::Vec3Array> points(float scale = DEFAULT_SCALE) const;

}; // class sptCore::StraightPath

class BezierPath: public Path
{
public:
    BezierPath(const osg::Vec3f& front, const osg::Vec3f& frontCP, const osg::Vec3f& back, const osg::Vec3f& backCP);
    BezierPath(const osg::Vec3f& front, const osg::Vec3f& frontCP, const osg::Vec3f& back, const osg::Vec3f& backCP, const float length);
    virtual ~BezierPath();

    virtual std::auto_ptr<Path> clone() const;
    virtual std::auto_ptr<Path> reverse() const;

    virtual osg::Vec3f frontDir() const;
    virtual osg::Vec3f backDir() const;

    virtual float length() const;
    virtual osg::ref_ptr<osg::Vec3Array> points(float scale = DEFAULT_SCALE) const;

    const osg::Vec3f& frontCP() const { return _frontCP; }
    const osg::Vec3f& backCP() const { return _backCP; }

private:
    osg::Vec3f _frontCP;
    osg::Vec3f _backCP;
    float _length;

    osg::ref_ptr<osg::Vec3Array> _points;

}; // class sptCore::BezierPath

} // namespace sptCore

#endif // headerguard
