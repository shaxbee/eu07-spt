#ifndef SPTGFX_EXTRUDER_H
#define SPTGFX_EXTRUDER_H 1

#include <osg/Geometry>

#include "sptCore/Path.h"

namespace sptGFX
{

//! Utility for extruding 2D profile along 3D path
class Extruder
{

public:
    //! Set up extruder
    //! \param profile geometry representing profile 
    //! \param primitiveSet index of primitive set in profile
    //! \param ignoredFaces number of faces ignored backwards (from last vertex)
    //! \warning PrimitiveSet used for extrusion must be osg::DrawElements instance in POLYGON mode 
    Extruder(osg::Geometry* profile, unsigned int primitiveSet, unsigned int ignoredFaces = 0): _profile(profile), _ignoredFaces(ignoredFaces) { };

    //! Extrude profile along path
    //! \param path extrusion path
    //! \param position vector added to all points
    //! \param offset deviation from axis of path
    //! \param texCoordOffset initial offset for texture coordinates
    void extrude(sptCore::Path& path, const osg::Vec3& position = osg::Vec3(), const osg::Vec3& offset = osg::Vec3(), double texCoordOffset = 0.0f);

    //! Set output geometry
    void setGeometry(osg::Geometry* geometry);

private:
    //! Generate vertex and texture positions
    void transformProfile(const osg::Vec3& position, const osg::Vec3& offset, osg::Vec3 direction, double texCoordY);

    osg::ref_ptr<osg::Geometry> _profile;
    osg::ref_ptr<osg::Geometry> _geometry;

    osg::ref_ptr<osg::Vec3Array> _vertices;
    osg::ref_ptr<osg::Vec2Array> _texCoords;

    unsigned int _ignoredFaces;

}; // class sptGFX::Extruder

} // namespace sptGFX

#endif // headerguard
