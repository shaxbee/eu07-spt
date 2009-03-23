#include "sptGFX/Extruder.h"

using namespace sptGFX;

osg::Geometry* Extruder::createGeometry(sptCore::Path* path, const osg::Vec3& offset)
{

    osg::Geometry* geometry = new osg::Geometry;

    osg::Vec3Array* vertices = new osg::Vec3Array;
    geometry->setVertexArray(vertices);

    int numProfileVerts = _profile->getNumElements();
    vertices->reserve(numProfileVerts * path->size());

    osg::Vec3Array::iterator iter = path->begin();
    osg::Vec3 prev = *iter;

    for(iter; iter != path->end(); iter++)
    {

        osg::Vec3 dir = *iter - prev;
        transformProfile(dir, prev + offset, vertices); 

        prev = *iter;

    };


    for(int index=0; index <= path->getNumElements(); index++)
    {

        geometry->addPrimitiveSet(new osg::DrawArrays(osg::PrimitiveSet::LINE_LOOP, index * numProfileVerts, numProfileVerts));

    };

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

    return geometry;

}; // Extruder::createPrimitiveSet

void Extruder::transformProfile(osg::Vec3 dir, const osg::Vec3& offset, osg::Vec3Array* output)
{

    dir.normalize();

    osg::Matrix transform = osg::Matrix::rotate(osg::Vec3(1.0f, 0.0f, 0.0f), dir);

    for(osg::Vec3Array::iterator iter = _profile->begin(); iter != _profile->end(); iter++)
        output->push_back((*iter + offset) * transform);

};
