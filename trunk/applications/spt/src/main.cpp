#include <osg/Geode>
#include <osgViewer/Viewer>

#include "sptCore/Path.h"
#include "sptGFX/Extruder.h"

using namespace sptCore;
using namespace sptGFX;

int main()
{
 
    osg::ref_ptr<osg::Geode> root = new osg::Geode;

    osg::Vec3 begin(0.0f,     0.0f, 0.0f);
    osg::Vec3 cpBegin(100.0f,   0.0f, 0.0f);
    osg::Vec3 end(100.0f, 100.0f, 0.0f);
    osg::Vec3 cpEnd(100.0f,   0.0f, 0.0f);

    Path* path = new Path(
        begin,
        cpBegin,
        end,
        cpEnd,
        32);

    {

        path->push_back(begin);
        path->push_back(cpBegin);
        path->push_back(end);
        path->push_back(cpEnd);

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

        int numElements = path->getNumElements() - 4;

        geometry->addPrimitiveSet(new osg::DrawArrays(osg::PrimitiveSet::LINE_STRIP, 0, numElements));
        geometry->addPrimitiveSet(new osg::DrawArrays(osg::PrimitiveSet::LINES, numElements, 4));

        root->addDrawable(geometry);

    };

    osg::Vec3Array* profile = new osg::Vec3Array;
    profile->push_back(osg::Vec3(-10.0f, 0.0f, 0.0f));
    profile->push_back(osg::Vec3(10.0f, 0.0f, 0.0f));
    profile->push_back(osg::Vec3(10.0f, 2.0f, 0.0f));
    profile->push_back(osg::Vec3(-10.0f, 2.0f, 0.0f));

    Extruder extruder(profile, 10.0f);
    root->addDrawable(extruder.createGeometry(path, osg::Vec3()));

    osgViewer::Viewer viewer;
    
    viewer.setSceneData(root.get());
    viewer.run();
    
    return 0;
    
}
