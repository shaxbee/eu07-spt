#include <iostream>

#include <osg/Geode>
#include <osg/PolygonMode>
#include <osgUtil/SmoothingVisitor>
#include <osgViewer/Viewer>

#include <sptCore/Path.h>
#include <sptCore/Track.h>

#include <sptCore/DynamicScenery.h>
#include <sptCore/DynamicSector.h>

#include "sptGFX/Extruder.h"

using namespace sptCore;
using namespace sptGFX;

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

int main()
{
 
    osg::ref_ptr<osg::Geode> root = new osg::Geode;

//    osg::StateSet* state = root->getOrCreateStateSet();
//    osg::PolygonMode* polygonMode = new osg::PolygonMode(osg::PolygonMode::FRONT_AND_BACK, osg::PolygonMode::LINE);
//    state->setAttribute(polygonMode);

    osg::Vec3 begin  (  0.0f,   0.0f, 0.0f);
    osg::Vec3 cpBegin(100.0f,   0.0f, 0.0f);
    osg::Vec3 end    (100.0f, 100.0f, 0.0f);
    osg::Vec3 cpEnd  (100.0f,   0.0f, 0.0f);

    Path* path = new Path(
        begin,
        cpBegin,
        end,
        cpEnd,
        20);

    {
        osg::Geometry* geometry = new osg::Geometry;
        geometry->setVertexArray(path);
        
        // set the colors as before, plus using the above
        osg::Vec4Array* colors = new osg::Vec4Array;
        colors->push_back(osg::Vec4(1.0f,1.0f,0.0f,1.0f));
        geometry->setColorArray(colors);
        geometry->setColorBinding(osg::Geometry::BIND_OVERALL);

        // set the normal in the same way color.
        osg::Vec3Array* normals = new osg::Vec3Array;
        normals->push_back(osg::Vec3(0.0f,-1.0f,0.0f));
        geometry->setNormalArray(normals);
        geometry->setNormalBinding(osg::Geometry::BIND_OVERALL);

        geometry->addPrimitiveSet(new osg::DrawArrays(osg::PrimitiveSet::LINE_STRIP, 0, path->getNumElements()));
        root->addDrawable(geometry);

    };

    DynamicScenery scenery;
    DynamicSector* sector = new DynamicSector(scenery, osg::Vec3());
    Track* track = new Track(*sector, osg::Vec3(0, 0, 0), osg::Vec3(100, 0, 0));

    sector->addTrack(track);
    scenery.addSector(sector);

    osg::ref_ptr<osg::Geometry> geometry = new osg::Geometry;
    geometry->setVertexArray(new osg::Vec3Array);
    geometry->setTexCoordArray(0, new osg::Vec2Array);

    osg::Vec4Array* colors = new osg::Vec4Array;
    colors->push_back(osg::Vec4(1.0f, 0.0f, 0.0f, 1.0f));
    geometry->setColorArray(colors);
    geometry->setColorBinding(osg::Geometry::BIND_OVERALL);

    osg::Geometry* profile(createProfile());
    Extruder::Settings settings;
//    settings.vertex.to = profile->getVertexArray()->getNumElements() - 2;
    Extruder extruder(profile, settings);
    extruder.setGeometry(geometry.get());

    extruder.extrude(*path);

    osgUtil::SmoothingVisitor::smooth(*geometry);

    root->addDrawable(geometry.get());

    osgViewer::Viewer viewer;
    
    viewer.setSceneData(root.get());
    viewer.run();
    
    return 0;
    
}
