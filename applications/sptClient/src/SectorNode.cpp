#include "SectorNode.h"
#include "SceneryAccess.h"

//#include <typeinfo>
#include <limits>

#include <osg/Geometry>
#include <osgUtil/SmoothingVisitor>

#include <sptGFX/Extruder.h>

#include <sptCore/Path.h>

#include <sptCore/TrackVisitor.h>
#include <sptCore/SimpleTrack.h>
#include <sptCore/Switch.h>

namespace
{

static osg::Vec3f INVALID_VEC3F = osg::Vec3f(
	std::numeric_limits<float>::infinity(),
	std::numeric_limits<float>::infinity(),
	std::numeric_limits<float>::infinity());

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

    osg::Vec4Array* colors = new osg::Vec4Array;
    colors->push_back(osg::Vec4(1.0f, 0.0f, 0.0f, 1.0f));
    geometry->setColorArray(colors);
    geometry->setColorBinding(osg::Geometry::BIND_OVERALL);

    sptGFX::Extruder::Settings settings;
//    settings.vertex.to = profile->getVertexArray()->getNumElements() - 2;
    sptGFX::Extruder extruder(profile, settings);
    extruder.setGeometry(geometry.get());

    extruder.extrude(*path);

    target->addDrawable(geometry.get());
};

class TrackGeometryVisitor: public sptCore::TrackVisitor
{
public:
    TrackGeometryVisitor(osg::Geode* target, osg::Geometry* profile):
        _target(target), _profile(profile)
    {
    }

    virtual void apply(const sptCore::SimpleTrack& value)
    {
        extrude(_target, _profile, value.getDefaultPath());
    }

    virtual void apply(const sptCore::Switch& value)
    {
    }

private:
    osg::ref_ptr<osg::Geode> _target;
    osg::ref_ptr<osg::Geometry> _profile;
}; // class TrackGeometryVisitor

};

SectorNode::SectorNode():
	Node(),
	_sector(INVALID_VEC3F),
	_geode()
{
}

SectorNode::SectorNode(const SectorNode& other, const osg::CopyOp& copyop):
	Node(),
	_sector(other._sector),
	_geode(new osg::Geode(*other._geode, copyop))
{
}

SectorNode::SectorNode(const osg::Vec3f& sector):
	Node(),
	_sector(sector),
	_geode(new osg::Geode())
{
	TrackGeometryVisitor visitor(_geode, createProfile());
    getSceneryInstance().getSector(_sector).accept(visitor);
}

void SectorNode::traverse(osg::NodeVisitor& visitor)
{
	_geode->accept(visitor);
}
