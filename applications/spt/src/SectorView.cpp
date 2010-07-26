#include "SectorView.h"

#include <sptCore/Path.h>

namespace 
{

void extrude(osg::Geode* target, osg::Geometry* profile, const sptCore::Path& path)
{

    osg::ref_ptr<osg::Geometry> geometry = new osg::Geometry;
    geometry->setVertexArray(new osg::Vec3Array);
    geometry->setTexCoordArray(0, new osg::Vec2Array);

    osg::Vec4Array* colors = new osg::Vec4Array;
    colors->push_back(osg::Vec4(1.0f, 0.0f, 0.0f, 1.0f));
    geometry->setColorArray(colors);
    geometry->setColorBinding(osg::Geometry::BIND_OVERALL);

    Extruder::Settings settings;
//    settings.vertex.to = profile->getVertexArray()->getNumElements() - 2;
    Extruder extruder(profile, settings);
    extruder.setGeometry(geometry.get());

    extruder.extrude(path);

    osgUtil::SmoothingVisitor::smooth(*geometry);

    target->addDrawable(geometry.get());

};

void SectorViewBuilder::visit(const sptCore::Track& tracking) 
{
    extrude(_target, _profile, tracking.getDefaultPath());
};

void SectorViewBuilder::visit(const sptCore::Switch& tracking) 
{ 
};

}; // anonymous namespace
