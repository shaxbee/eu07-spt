#include <osg/Geometry>
#include <osg/Geode>

#include <osg/PolygonMode>
#include <osg/PolygonOffset>
#include <osg/Material>
#include <osg/LineWidth>
#include <osg/Texture2D>

#include <osgDB/ReadFile>
#include <osgDB/WriteFile>

#include <osgViewer/Viewer>

#include "sptCore/Path.h"
#include "sptGFX/Extruder.h"

#if 0
namespace sptView
{

struct TrackMaterialComponent
{
	sptGFX::Extruder::Settings settings;
	sptGFX::Extruder::Profile profile;
	osg::ref_ptr<osg::StateSet> stateSet;
};

struct TrackMaterial
{
	typedef std::vector<TrackMaterialComponent> Components;
	Components components;
};
}
#endif

osg::Geometry* createProfile()
{

    osg::Geometry* geometry = new osg::Geometry;

    osg::Vec3Array* vertices = new osg::Vec3Array;
    vertices->push_back(osg::Vec3(-1.2f, 0.0f, 0.0f));
    vertices->push_back(osg::Vec3(-0.8f, 0.0f, 0.5f));
    vertices->push_back(osg::Vec3( 0.8f, 0.0f, 0.5f));
    vertices->push_back(osg::Vec3( 1.2f, 0.0f, 0.0f));
    geometry->setVertexArray(vertices);

    osg::Vec2Array* texCoords = new osg::Vec2Array;
    texCoords->push_back(osg::Vec2(0.0f, 0.0f));
    texCoords->push_back(osg::Vec2(0.7f / 3.0f, 0.0f));
    texCoords->push_back(osg::Vec2(2.3f / 3.0f, 0.0f));
    texCoords->push_back(osg::Vec2(1.0f, 0.0f));
    geometry->setTexCoordArray(0, texCoords);

    return geometry;

};

void extrude(osg::Geode* target, osg::Geometry* profile, std::unique_ptr<sptCore::Path> path)
{
    osg::ref_ptr<osg::Geometry> geometry(new osg::Geometry);

    geometry->setVertexArray(new osg::Vec3Array);
    geometry->setNormalArray(new osg::Vec3Array);
    geometry->setNormalBinding(osg::Geometry::BIND_PER_VERTEX);
    geometry->setTexCoordArray(0, new osg::Vec2Array);

    sptGFX::Extruder::Settings settings;
    settings.texture.scale = osg::Vec2f(1.0, 0.25);

    sptGFX::Extruder extruder(profile, geometry.get(), settings);

    geometry->addPrimitiveSet(extruder.extrude(*path));

    target->addDrawable(geometry.get());
};

osg::ref_ptr<osg::Group> wireframeDecorator(osg::ref_ptr<osg::Node> node)
{
	osg::ref_ptr<osg::Group> decorator(new osg::Group);
	osg::ref_ptr<osg::StateSet> stateSet(decorator->getOrCreateStateSet());

	stateSet->setAttribute(new osg::LineWidth(2.0f));
	stateSet->setAttributeAndModes(new osg::PolygonOffset(-1.0f, -1.0f), osg::StateAttribute::OVERRIDE | osg::StateAttribute::ON);
	stateSet->setAttributeAndModes(new osg::PolygonMode(osg::PolygonMode::FRONT_AND_BACK, osg::PolygonMode::LINE), osg::StateAttribute::OVERRIDE | osg::StateAttribute::ON);
	stateSet->setAttributeAndModes(new osg::Material, osg::StateAttribute::OVERRIDE | osg::StateAttribute::ON);
	stateSet->setMode(GL_LIGHTING,osg::StateAttribute::OVERRIDE|osg::StateAttribute::OFF);
	stateSet->setTextureMode(0,GL_TEXTURE_2D,osg::StateAttribute::OVERRIDE|osg::StateAttribute::OFF);

	decorator->addChild(node);

	return decorator;
}

int main()
{
    osg::ref_ptr<osg::Group> root(new osg::Group);

    osg::ref_ptr<osg::Geode> track(new osg::Geode);
    osg::ref_ptr<osg::Geometry> profile(createProfile());

    osg::ref_ptr<osg::StateSet> stateSet(track->getOrCreateStateSet());

    osg::ref_ptr<osg::Texture2D> tex0(new osg::Texture2D(osgDB::readImageFile("tpd-oil1.tga")));
    tex0->setWrap(osg::Texture2D::WRAP_T, osg::Texture2D::REPEAT);
    stateSet->setTextureAttribute(0, tex0.get());

    osg::ref_ptr<osg::Texture2D> tex1(new osg::Texture2D(osgDB::readImageFile("tpbp-new2.tga")));
    tex1->setWrap(osg::Texture2D::WRAP_T, osg::Texture2D::REPEAT);
    stateSet->setTextureAttribute(1, tex1.get());

    char vertexShaderSource[] =
       "varying vec2 texCoord;\n"
       "void main(void)\n"
       "{\n"
       "    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;\n"
       "    texCoord = gl_MultiTexCoord0.xy;\n"
       "}\n";

    char fragmentShaderSource[] =
        "varying vec2 texCoord;\n"
        "uniform sampler2D texLeft;\n"
    	"uniform sampler2D texRight;\n"
    	"uniform float blendPoint;\n"
    	"uniform float blendSize;\n"
        "\n"
        "void main(void)\n"
        "{\n"
    	"    vec4 c0 = texture2D(texLeft, texCoord); \n"
        "    vec4 c1 = texture2D(texRight, texCoord); \n"
    	"    float blend = (texCoord.t - blendPoint + blendSize) / (2.0f * blendSize); \n"
        "    gl_FragColor = mix(c0, c1, clamp(blend, 0.0f, 1.0f)); \n"
        "}\n";

    osg::ref_ptr<osg::Program> program(new osg::Program);
    program->addShader(new osg::Shader(osg::Shader::VERTEX, vertexShaderSource));
    program->addShader(new osg::Shader(osg::Shader::FRAGMENT, fragmentShaderSource));

    stateSet->addUniform(new osg::Uniform("blendPoint", 20.0f));
    stateSet->addUniform(new osg::Uniform("blendSize", 0.4f));
    stateSet->setAttribute(program.get());

#if 1
    std::unique_ptr<sptCore::Path> path(new sptCore::BezierPath(
        osg::Vec3(0.0, 0.0, 0.0),
        osg::Vec3(100.0, 0.0, 0.0),
        osg::Vec3(100.0, 100.0, 0.0),
        osg::Vec3(0.0, 100.0, 0.0)
    ));
#else
    std::unique_ptr<sptCore::Path> path(new sptCore::StraightPath(
        osg::Vec3(0.0, 0.0, 0.0),
        osg::Vec3(100.0, 0.0, 0.0)
    ));
#endif


    extrude(track.get(), profile.get(), path->clone());

    root->addChild(track);
    root->addChild(wireframeDecorator(track));

    osgViewer::Viewer viewer;
    viewer.setSceneData(root);
    return viewer.run();
}
