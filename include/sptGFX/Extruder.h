#ifndef SPTGFX_EXTRUDER_H
#define SPTGFX_EXTRUDER_H 1

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
    Extruder(const osg::Geometry* profile, osg::Geometry* output, const Settings& settings);
    
    const Settings& getSettings() const { return _settings; }

    //! \brief Extrude profile along path
    //! Create PrimitiveSet basing on provided settings and add it to geometry
    //! \param path extrusion path
    //! \param position vector added to all points
    //! \param offset deviation from axis of path
    //! \param texCoordOffset initial offset for texture coordinates
    osg::ref_ptr<osg::PrimitiveSet> extrude(const sptCore::Path& path, const osg::Vec3& position = osg::Vec3());
    
    //! \brief Extruding settings
    struct Settings
    {

    	Settings(): vertex(), texture() { };

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

        Vertex vertex;
        Texture texture;
        
    }; // sptGFX::Extruder::Settings

	struct Profile
	{
		Profile(const osg::Geometry* profile);

		const osg::Vec3Array& vertices;
		const osg::Vec2Array& texCoords;
	};

	struct Output
	{
		Output(osg::Geometry* output);

		osg::Vec3Array& vertices;
		osg::Vec3Array& normals;
		osg::Vec2Array& texCoords;
	};

    struct State
    {
    	State(): numVerts(0), texCoordT(0.0f) { };

    	size_t numVerts;
    	float texCoordT;
    };

private:
    //! Generate vertex and texture positions
    void transformProfile(const osg::Vec3& position, osg::Vec3 direction);

    const Settings _settings;

    const Profile _profile;
    Output _output;
    State _state;

}; // class sptGFX::Extruder

} // namespace sptGFX

#endif // headerguard
