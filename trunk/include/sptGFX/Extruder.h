#ifndef SPTGFX_EXTRUDER_H
#define SPTGFX_EXTRUDER_H 1

#include <osg/Geometry>

#include "sptCore/Path.h"

namespace sptGFX
{

class Extruder
{

public:
    Extruder(osg::Vec3Array* profile, float segmentLength): 
        _profile(profile), _segmentLength(segmentLength) { }

    osg::Geometry* createGeometry(sptCore::Path* path, const osg::Vec3& offset);

private:
    void transformProfile(osg::Vec3 dir, const osg::Vec3& offset, osg::Vec3Array* output);

    osg::ref_ptr<osg::Vec3Array> _profile;
    float _segmentLength; 

}; // class sptGFX::Extruder

} // namespace sptGFX

#endif // headerguard
