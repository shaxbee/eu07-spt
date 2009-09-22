#ifndef SPTGFX_EXTRUDER_H
#define SPTGFX_EXTRUDER_H 1

#include <limits>

#include <osg/Vec2d>
#include <osg/Geometry>

#include <sptCore/Path.h>

namespace sptGFX
{
    
//! Utility for extruding 2D profile along 3D path
class Extruder
{

public:
    struct Settings;
    //! \brief Set up extruder
    //! \param profile geometry representing profile 
    //! \param primitiveSet index of primitive set in profile
    //! \param ignoredFaces number of faces ignored backwards (from last vertex)
    //! \warning PrimitiveSet used for extrusion must be osg::DrawElements instance in POLYGON mode 
    Extruder(osg::Geometry* profile, const Settings& settings);
    
    //!
    const Settings& getSettings() const { return _settings; }

    //! \brief Extrude profile along path
    //! Create PrimitiveSet basing on provided settings and add it to geometry
    //! \param path extrusion path
    //! \param position vector added to all points
    //! \param offset deviation from axis of path
    //! \param texCoordOffset initial offset for texture coordinates
    void extrude(sptCore::Path& path, const osg::Vec3& position = osg::Vec3(), const osg::Vec3& offset = osg::Vec3(), double texCoordOffset = 0.0f);

    //! Set output geometry
    void setGeometry(osg::Geometry* geometry);
    
    //! \brief Extruding settings
    struct Settings
    {

        struct Vertex 
        {
            Vertex(): scale(1.0f, 1.0f, 1.0f), primitiveSet(0), from(0), to(std::numeric_limits<unsigned int>::max()) { };

            //! \brief Object scale
            osg::Vec3 scale;
            //! \brief Index of primitive set in profile
            unsigned int primitiveSet;
            //! \brief Index of first profile vertex
            unsigned int from;
            //! \brief Index of last profile vertex
            unsigned int to;
        };
    	
        struct Texture
        {
            Texture(): unit(0), offset(), scale(1.0f, 1.0f) { };

            //! \brief Texture unit index
            unsigned int unit;
            //! \brief UV coordinates offset
            osg::Vec2d offset;
            //! \brief UV coordinates scale
            osg::Vec2d scale;
        };
    		
    	Vertex vertex;
        Texture texture;
        
    }; // sptGFX::Extruder::Settings

private:
    //! Generate vertex and texture positions
    void transformProfile(const osg::Vec3& position, const osg::Vec3& offset, osg::Vec3 direction, double texCoordY);

    inline unsigned int vertsCount() { return _settings.vertex.to - _settings.vertex.from; };

    osg::ref_ptr<osg::Geometry> _profile;
    osg::ref_ptr<osg::Geometry> _geometry;

    osg::ref_ptr<osg::Vec3Array> _vertices;
    osg::ref_ptr<osg::Vec2Array> _texCoords;

    Settings _settings;

}; // class sptGFX::Extruder

} // namespace sptGFX

#endif // headerguard
