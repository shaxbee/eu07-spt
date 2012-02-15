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
    //! \param settings vertex and texture settings 
    //! \warning PrimitiveSet used for extrusion must be osg::DrawElements instance in POLYGON mode 
    Extruder(osg::Geometry* profile, const Settings& settings);
    
    const Settings& getSettings() const { return _settings; }

    //! \brief Extrude profile along path
    //! Create PrimitiveSet basing on provided settings and add it to geometry
    //! \param path extrusion path
    //! \param position vector added to all points
    //! \param offset deviation from axis of path
    //! \param texCoordOffset initial offset for texture coordinates
    void extrude(const sptCore::Path& path, const osg::Vec3& position = osg::Vec3());

    //! \brief Set output geometry
    void setGeometry(osg::Geometry* geometry);
    
    //! \brief Extruding settings
    struct Settings
    {

    	enum Mode
    	{
    		LOOP,
    		STRIP
    	};

        struct Vertex 
        {
            Vertex(): scale(1.0f, 1.0f, 1.0f) { };

            //! Vertex offset
            osg::Vec3 offset;

            //! Vertex scale
            osg::Vec3 scale;

        };
        
        struct Texture
        {
            Texture(): offset(), scale(1.0f, 1.0f) { };

            //! ST coordinates offset
            osg::Vec2d offset;
            //! ST coordinates scale
            osg::Vec2d scale;
        };

        Mode mode;
        Vertex vertex;
        Texture texture;
        
    }; // sptGFX::Extruder::Settings

    struct State
    {
    	State(): numVerts(0), texCoordT(0.0f) { };

    	size_t numVerts;
    	float texCoordT;
    };

private:
    //! Generate vertex and texture positions
    void transformProfile(const osg::Vec3& position, osg::Vec3 direction);
    const osg::Vec3f& getVertex(size_t index) const;

    osg::ref_ptr<osg::Geometry> _profile;
    osg::ref_ptr<osg::Geometry> _geometry;

    osg::ref_ptr<osg::Vec3Array> _vertices;
    osg::ref_ptr<osg::Vec2Array> _texCoords;

    Settings _settings;
    State _state;

}; // class sptGFX::Extruder

} // namespace sptGFX

#endif // headerguard
