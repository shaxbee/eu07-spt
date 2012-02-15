#include <sptGFX/Extruder.h>
#include <sptUtil/Math.h>

#include <cassert>

//#include <iterator>
//#include <iostream>
//#include <osg/io_utils>

using namespace sptGFX;

Extruder::Extruder(osg::Geometry* profile, const Settings& settings):
    _profile(profile),
    _settings(settings)
{
}; // Extruder::Extruder

const osg::Vec3f& Extruder::getVertex(size_t index) const
{
    assert(_vertices);
    return (*_vertices)[index];
};

void Extruder::setGeometry(osg::Geometry* geometry)
{

    _geometry = geometry;

    _vertices = static_cast<osg::Vec3Array*>(geometry->getVertexArray());
    _texCoords = static_cast<osg::Vec2Array*>(geometry->getTexCoordArray(0));

};

void Extruder::extrude(const sptCore::Path& path, const osg::Vec3& position)
{

    size_t numProfileVerts = _profile->getVertexArray()->getNumElements();

    osg::ref_ptr<osg::Vec3Array> points(path.points());
    size_t numPathVerts = points->getNumElements() - 1;

    // resize vertices and texture coordinate arrays
    {
        size_t numVerts = numProfileVerts * numPathVerts;

        _vertices->reserve(_vertices->size() + numVerts);
        _texCoords->reserve(_texCoords->size() + numVerts);
    }

    // first profile
    transformProfile(path.front(), path.frontDir());

    osg::Vec3 prev = path.front();

    // profiles from second
    for(size_t row = 1; row < numPathVerts - 1; row++)
    {
        osg::Vec3 point = (*points)[row];
        osg::Vec3 dir = point - prev;
        _state.texCoordT += dir.length();

        transformProfile(point, dir);

        prev = point;
    };

    // last profile
    _state.texCoordT += (path.back() - prev).length();
    transformProfile(path.back(), path.backDir());

//    std::copy(_vertices->begin(), _vertices->end(), std::ostream_iterator<osg::Vec3f>(std::cout, "\n"));

    size_t numFaces = (numProfileVerts - 1) * (numPathVerts - 1);

    osg::Vec3Array* normals = new osg::Vec3Array(numFaces * 2);
    osg::DrawElementsUInt* primitiveSet = new osg::DrawElementsUInt(osg::PrimitiveSet::TRIANGLES, 0);

    for(size_t row = 0; row < numPathVerts - 1; row++)
    {
    	for(size_t face = 0; face < numProfileVerts - 2; face++)
    	{
    		size_t index = row * numProfileVerts + face;

			// first triangle
			primitiveSet->push_back(index);
			primitiveSet->push_back(index + 1);
			primitiveSet->push_back(index + numProfileVerts);

			// second triangle
			primitiveSet->push_back(index + 1);
			primitiveSet->push_back(index + numProfileVerts);
			primitiveSet->push_back(index + numProfileVerts + 1);

			// normal - cross product of face X and Z axis edges
			osg::Vec3f normal(
				(getVertex(index + 1) - getVertex(index)) ^ // X edge
				(getVertex(index) - getVertex(index + numProfileVerts)) // Z edge;
			);

			// normal vector should have length of 1
			normal.normalize();

			// same normal vector for two triangles per face
			normals->push_back(-normal);
			normals->push_back(-normal);
    	};
    };

    // _geometry->setNormalArray(normals);
    _geometry->addPrimitiveSet(primitiveSet);
}; // Extruder::createPrimitiveSet

void Extruder::transformProfile(const osg::Vec3& position, osg::Vec3 direction)
{

    osg::Vec3Array& profileVertices = static_cast<osg::Vec3Array&>(*(_profile->getVertexArray()));
    osg::Vec2Array& profileTexCoords = static_cast<osg::Vec2Array&>(*(_profile->getTexCoordArray(0)));

    osg::Matrix transform(sptUtil::rotationMatrix(direction));

    for(size_t index = 0; index < profileVertices.getNumElements(); index++)
    {
        _vertices->push_back(transform * (profileVertices[index] + _settings.vertex.offset) + position);

        osg::Vec2f texCoord(profileTexCoords[index] + osg::Vec2(0, _state.texCoordT) + _settings.texture.offset);
        _texCoords->push_back(osg::Vec2f(
        	texCoord.x() * _settings.texture.scale.x(),
        	texCoord.y() * _settings.texture.scale.y()));
    };

};
