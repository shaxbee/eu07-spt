#include <osg/Geometry>
#include <osg/Geode>

#include <osg/PolygonMode>
#include <osg/PolygonOffset>
#include <osg/Material>
#include <osg/LineWidth>
#include <osg/Texture2D>

#include <osgDB/ReadFile>
#include <osgViewer/Viewer>

#include "sptCore/Path.h"
#include "sptGFX/Extruder.h"

osg::Geometry* createProfile()
{

    osg::Geometry* geometry = new osg::Geometry;

    osg::Vec3Array* vertices = new osg::Vec3Array;
    vertices->push_back(osg::Vec3(-1.2f, 0.0f, 0.0f));
    vertices->push_back(osg::Vec3(-0.8f, 0.0f, 0.5f));
    vertices->push_back(osg::Vec3( 0.8f, 0.0f, 0.5f));
    vertices->push_back(osg::Vec3( 1.2f, 0.0f, 0.0f));
    vertices->push_back(osg::Vec3(-1.2f, 0.0f, 0.0f));
    geometry->setVertexArray(vertices);

    osg::Vec2Array* texCoords = new osg::Vec2Array;
    texCoords->push_back(osg::Vec2(0.0f, 0.0f));
    texCoords->push_back(osg::Vec2(0.7f / 3.0f, 0.0f));
    texCoords->push_back(osg::Vec2(2.3f / 3.0f, 0.0f));
    texCoords->push_back(osg::Vec2(1.0f, 0.0f));
    texCoords->push_back(osg::Vec2(0.0f, 0.0f));
    geometry->setTexCoordArray(0, texCoords);

    return geometry;

};

void extrude(osg::Geode* target, osg::Geometry* profile, std::auto_ptr<sptCore::Path> path)
{
    osg::ref_ptr<osg::Geometry> geometry = new osg::Geometry;
    geometry->setVertexArray(new osg::Vec3Array);
    geometry->setTexCoordArray(0, new osg::Vec2Array);
    geometry->setNormalBinding(osg::Geometry::BIND_PER_PRIMITIVE);

    sptGFX::Extruder::Settings settings;
    settings.texture.scale = osg::Vec2f(1.0, 0.25);

    sptGFX::Extruder extruder(profile, settings);
    extruder.setGeometry(geometry.get());

    extruder.extrude(*path);

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

    osg::ref_ptr<osg::Texture2D> texture(new osg::Texture2D(osgDB::readImageFile("tpd-oil1.tga")));
    texture->setWrap(osg::Texture2D::WRAP_T, osg::Texture2D::REPEAT);
    track->getOrCreateStateSet()->setTextureAttribute(0, texture.get());

    std::auto_ptr<sptCore::Path> path(new sptCore::BezierPath(
        osg::Vec3(0.0, 0.0, 0.0),
        osg::Vec3(100.0, 0.0, 0.0),
        osg::Vec3(100.0, 100.0, 0.0),
        osg::Vec3(0.0, 100.0, 0.0)
    ));

    extrude(track.get(), profile.get(), path->clone());

    root->addChild(track);
    root->addChild(wireframeDecorator(track));

    osgViewer::Viewer viewer;
    viewer.setSceneData(root);
    return viewer.run();
}
