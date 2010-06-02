#include <iostream>

#include <osg/Geode>
#include <osg/PolygonMode>
#include <osg/LineWidth>

#include <osgUtil/SmoothingVisitor>
#include <osgViewer/Viewer>

#include <sptCore/Path.h>
#include <sptGFX/Extruder.h>

using namespace sptCore;
using namespace sptGFX;

void print_vec(const osg::Vec3& vec)
{
    std::cout << vec.x() << " " << vec.y() << " " << vec.z() << std::endl;
}

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

osg::Geode* createAxes(osg::Geode* geode)
{

    osg::BoundingBox box = geode->getBoundingBox();
    box.expandBy(osg::BoundingBox(box.corner(0), box.corner(0) + osg::Vec3(100, 100, 100)));

    osg::Vec4 red(1.0f, 0.0f, 0.0f, 1.0f);
    osg::Vec4 green(0.0f, 1.0f, 0.0f, 1.0f);
    osg::Vec4 blue(0.0f, 0.0f, 1.0f, 1.0f);
   
    osg::Geode* result = new osg::Geode; 
    osg::Geometry* geometry = new osg::Geometry;

    osg::Vec3Array* vertices = new osg::Vec3Array;
    osg::Vec4Array* colors = new osg::Vec4Array;

    osg::Vec3Array* normals = new osg::Vec3Array;
    normals->push_back(osg::Vec3(0.0f,-1.0f,0.0f));

    // X axis
    vertices->push_back(box.corner(0));
    vertices->push_back(box.corner(1));
    colors->push_back(red);
    colors->push_back(red);

    // Y axis
    vertices->push_back(box.corner(0));
    vertices->push_back(box.corner(2));
    colors->push_back(green);
    colors->push_back(green);

    // Z axis
    vertices->push_back(box.corner(0));
    vertices->push_back(box.corner(4));
    colors->push_back(blue);
    colors->push_back(blue);

    // compose geometry
    geometry->setVertexArray(vertices);

    geometry->setColorArray(colors);
    geometry->setColorBinding(osg::Geometry::BIND_PER_VERTEX);

    geometry->setNormalArray(normals);
    geometry->setNormalBinding(osg::Geometry::BIND_OVERALL);
        
    geometry->addPrimitiveSet(new osg::DrawArrays(osg::PrimitiveSet::LINES, 0, vertices->getNumElements()));

    osg::StateSet* stateSet = new osg::StateSet;
    stateSet->setAttribute(new osg::LineWidth(3));

    result->setStateSet(stateSet);

    // add geometry to geode
    result->addDrawable(geometry);

    return result;
};

int main()
{
 
    osg::ref_ptr<osg::Group> root = new osg::Group;
    osg::ref_ptr<osg::Geode> geode = new osg::Geode;

//    osg::StateSet* state = root->getOrCreateStateSet();
//    osg::PolygonMode* polygonMode = new osg::PolygonMode(osg::PolygonMode::FRONT_AND_BACK, osg::PolygonMode::LINE);
//    state->setAttribute(polygonMode);

    osg::Vec3 begin  (  0.0f,   0.0f, 0.0f);
    osg::Vec3 cpBegin(100.0f,   0.0f, 0.0f);
    osg::Vec3 end    (100.0f, 100.0f, 0.0f);
    osg::Vec3 cpEnd  (100.0f,   0.0f, 0.0f);

    Path* path = new BezierPath(
        begin,
        cpBegin,
        end,
        cpEnd);
//        40);

    print_vec(path->frontDir());
    print_vec(path->backDir());

    {
        osg::Geometry* geometry = new osg::Geometry;
        geometry->setVertexArray(path->points());
        
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

        geometry->addPrimitiveSet(new osg::DrawArrays(osg::PrimitiveSet::LINE_STRIP, 0, path->points()->getNumElements()));
        geode->addDrawable(geometry);

    };

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

    geode->addDrawable(geometry.get());
    root->addChild(geode.get());
    root->addChild(createAxes(geode.get()));

    osgViewer::Viewer viewer;
    
    viewer.setSceneData(root.get());
    viewer.run();
    
    return 0;
    
}
