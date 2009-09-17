#include "sptGFX/Extruder.h"

#include <iostream>
#include <osgUtil/SmoothingVisitor>

using namespace sptGFX;

void Extruder::setGeometry(osg::Geometry* geometry)
{

    _geometry = geometry;

    _vertices = static_cast<osg::Vec3Array*>(geometry->getVertexArray());
    _texCoords = static_cast<osg::Vec2Array*>(geometry->getTexCoordArray(0));

};

void Extruder::extrude(sptCore::Path& path, const osg::Vec3& position, const osg::Vec3& offset, double texCoordOffset)
{

    size_t numProfileVerts = _profile->getVertexArray()->getNumElements();
    size_t numPathVerts = path.getNumElements();

    // resize vertices and texture coordinate arrays
    {

        size_t numVerts = numProfileVerts * numPathVerts;

        _vertices->reserve(_vertices->size() + numVerts);
        _texCoords->reserve(_texCoords->size() + numVerts);

    }

    double texCoordY = texCoordOffset;

    // first profile
    transformProfile(path.front(), offset, path.frontDir(), texCoordY);

    osg::Vec3 prev = path.front();

    // profiles from second
    for(size_t row = 1; row < numPathVerts - 1; row++)
    {

        osg::Vec3 point = path[row]; 
        osg::Vec3 direction = point - prev;
        texCoordY += direction.length();

        transformProfile(point, offset, direction, texCoordY);

        prev = point;

    };

    // last profile
    texCoordY += (path.back() - prev).length(); 
    transformProfile(path.back(), offset, path.backDir(), texCoordY);

    // create faces index arrays
    for(size_t face = 0; face < numProfileVerts - _ignoredFaces - 1; face++)
    {

        osg::DrawElementsUInt* primitiveSet = new osg::DrawElementsUInt(GL_TRIANGLE_STRIP, numPathVerts * 2);
            
        for(size_t row=0; row < numPathVerts; row++)
        {
            size_t index = row * (numProfileVerts - _ignoredFaces) + face;

            std::cout << index << " " << index + 1 << std::endl;

            primitiveSet->push_back(index);
            primitiveSet->push_back(index + 1);
        };

        _geometry->addPrimitiveSet(primitiveSet);

    };

    std::cout << numProfileVerts << " " << _vertices->getNumElements() << " " << (numProfileVerts - _ignoredFaces) * numPathVerts << std::endl;

}; // Extruder::createPrimitiveSet

void Extruder::transformProfile(const osg::Vec3& position, const osg::Vec3& offset, osg::Vec3 direction, double texCoordY)
{

    osg::Vec3Array& profileVertices = static_cast<osg::Vec3Array&>(*(_profile->getVertexArray()));
    osg::Vec2Array& profileTexCoords = static_cast<osg::Vec2Array&>(*(_profile->getTexCoordArray(0)));

    direction.normalize();

    osg::Quat transform;
    transform.makeRotate(osg::X_AXIS, direction);

    for(size_t index = 0; index < profileVertices.getNumElements() - _ignoredFaces; index++)
    {

        _vertices->push_back(transform * (profileVertices[index] + offset) + position);
        _texCoords->push_back(profileTexCoords[index] + osg::Vec2(0, texCoordY));

    };

};
