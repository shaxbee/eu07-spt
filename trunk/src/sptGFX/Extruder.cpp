#include <sptGFX/Extruder.h>

#include <iostream>
#include <osgUtil/SmoothingVisitor>

#include <sptCore/Math.h>

using namespace sptGFX;

Extruder::Extruder(osg::Geometry* profile, const Settings& settings):
    _profile(profile),
    _settings(settings)
{

    if(_settings.vertex.to == std::numeric_limits<unsigned int>::max())
        _settings.vertex.to = profile->getVertexArray()->getNumElements() - 1;

}; // Extruder::Extruder

void Extruder::setGeometry(osg::Geometry* geometry)
{

    _geometry = geometry;

    _vertices = static_cast<osg::Vec3Array*>(geometry->getVertexArray());
    _texCoords = static_cast<osg::Vec2Array*>(geometry->getTexCoordArray(0));

};

void Extruder::extrude(sptCore::Path& path, const osg::Vec3& position, const osg::Vec3& offset, double texCoordOffset)
{

    size_t numProfileVerts = vertsCount();
    size_t numPathVerts = path.getNumElements();

    std::cout << numProfileVerts << std::endl;

    // resize vertices and texture coordinate arrays
    {

        size_t numVerts = numProfileVerts * numPathVerts;

        _vertices->reserve(_vertices->size() + numVerts);
        _texCoords->reserve(_texCoords->size() + numVerts);

    }

    double texCoordV = texCoordOffset;

    // first profile
    transformProfile(path.front(), offset, path.frontDir(), texCoordV);

    osg::Vec3 prev = path.front();

    // profiles from second
    for(size_t row = 1; row < numPathVerts - 1; row++)
    {

        osg::Vec3 point = path[row]; 
        osg::Vec3 dir = point - prev;
        texCoordV += dir.length();

        transformProfile(point, offset, dir, texCoordV);

        prev = point;

    };

    // last profile
    texCoordV += (path.back() - prev).length(); 
    transformProfile(path.back(), offset, path.backDir(), texCoordV);

    std::cout << path.back().x() << " " << path.back().y() << std::endl;
    std::cout << _vertices->getNumElements() << std::endl;

    // create faces index arrays
    for(size_t face = 0; face < numProfileVerts - 1; face++)
    {

        osg::DrawElementsUInt* primitiveSet = new osg::DrawElementsUInt(GL_TRIANGLE_STRIP, numPathVerts * 2);
            
        for(size_t row=0; row < numPathVerts; row++)
        {
            size_t index = row * numProfileVerts + face;

            primitiveSet->push_back(index);
            primitiveSet->push_back(index + 1);
        };

        _geometry->addPrimitiveSet(primitiveSet);

    };

}; // Extruder::createPrimitiveSet

void Extruder::transformProfile(const osg::Vec3& position, const osg::Vec3& offset, osg::Vec3 direction, double texCoordV)
{

    osg::Vec3Array& profileVertices = static_cast<osg::Vec3Array&>(*(_profile->getVertexArray()));
    osg::Vec2Array& profileTexCoords = static_cast<osg::Vec2Array&>(*(_profile->getTexCoordArray(0)));

    osg::Matrix transform(sptCore::rotationMatrix(direction));

    for(size_t index = _settings.vertex.from; index < _settings.vertex.to; index++)
    {

        _vertices->push_back(transform * (profileVertices[index] + offset) + position);
        _texCoords->push_back(profileTexCoords[index] + osg::Vec2(0, texCoordV));

    };

};
