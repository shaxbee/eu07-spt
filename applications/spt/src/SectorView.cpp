#include "SectorView.h"

#include <osg/Geometry>
#include <osgUtil/SmoothingVisitor>

#include <sptGFX/Extruder.h>

#include <sptCore/Path.h>
#include <sptCore/Track.h>
#include <sptCore/Switch.h>

#include <iostream>

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

    sptGFX::Extruder::Settings settings;
//    settings.vertex.to = profile->getVertexArray()->getNumElements() - 2;
    sptGFX::Extruder extruder(profile, settings);
    extruder.setGeometry(geometry.get());

    extruder.extrude(path);

    osgUtil::SmoothingVisitor::smooth(*geometry);

    target->addDrawable(geometry.get());

};

};

void SectorViewBuilder::visit(const sptCore::Track& tracking) 
{
    std::cout << "track" << std::endl;
    extrude(_target.get(), _profile.get(), tracking.getDefaultPath());
};

void SectorViewBuilder::visit(const sptCore::Switch& tracking) 
{ 
};

