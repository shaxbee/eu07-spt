#include "view/SectorView.h"

#include <typeinfo>

#include <osg/Geometry>
#include <osgUtil/SmoothingVisitor>

#include <sptGFX/Extruder.h>

#include <sptCore/Path.h>
#include <sptCore/Track.h>
#include <sptCore/Switch.h>

namespace 
{

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

};

void createSectorGeometry(osg::Geode* target, osg::Geometry* profile, const sptCore::Sector& sector)
{
    for(unsigned int index = 0; index != sector.getRailTrackingCount(); index++)
    {
        const sptCore::Track& tracking = sector.getRailTracking(index);
        if(typeid(tracking) == typeid(sptCore::SimpleTrack))
        {
            const sptCore::SimpleTrack& track = static_cast<const sptCore::SimpleTrack&>(tracking);
            extrude(target, profile, track.getDefaultPath());
        };
    };
};
