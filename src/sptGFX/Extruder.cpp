#include <sptGFX/Extruder.h>
#include <sptUtil/Math.h>

#include <cassert>
#include <iostream>

using namespace sptGFX;

Extruder::Profile::Profile(const osg::Geometry* profile):
	vertices(static_cast<const osg::Vec3Array&>(*(profile->getVertexArray()))),
	texCoords(static_cast<const osg::Vec2Array&>(*(profile->getTexCoordArray(0))))
{
	assert(profile->getVertexArray() && profile->getTexCoordArray(0));
}

Extruder::Output::Output(osg::Geometry* output):
	vertices(static_cast<osg::Vec3Array&>(*(output->getVertexArray()))),
	normals(static_cast<osg::Vec3Array&>(*(output->getNormalArray()))),
	texCoords(static_cast<osg::Vec2Array&>(*output->getTexCoordArray(0)))
{
	assert(output->getVertexArray() && output->getNormalArray() && output->getTexCoordArray(0));
}

Extruder::Extruder(const osg::Geometry* profile, osg::Geometry* output, const Settings& settings):
    _settings(settings),
    _profile(profile),
    _output(output),
    _state()
{
}; // Extruder::Extruder

osg::ref_ptr<osg::PrimitiveSet> Extruder::extrude(const sptCore::Path& path, const osg::Vec3& position)
{
    osg::ref_ptr<osg::Vec3Array> points(path.points());
    size_t numPathVerts = points->getNumElements();
    size_t numProfileVerts = _profile.vertices.getNumElements();

    size_t prevNumVerts = _output.vertices.size();
    size_t numVerts = numProfileVerts * numPathVerts;

    // resize vertices and texture coordinate arrays
    {
		_output.vertices.reserve(prevNumVerts + numVerts);
		_output.normals.resize(prevNumVerts + numVerts);
		_output.texCoords.reserve(prevNumVerts + numVerts);
    };

    // create vertices
    {
		// first profile
    	osg::Vec3Array::const_iterator iter = points->begin();
		transformProfile(*iter, path.frontDir());

		osg::Vec3 prev = *iter;

		// profiles from second
		for(iter++; iter != points->end() - 1; iter++)
		{
			osg::Vec3 point(*iter);
			osg::Vec3 dir(point - prev);
			_state.texCoordT += dir.length();

			transformProfile(point, dir);

			prev = point;
		};

		// last profile
		_state.texCoordT += (*iter - prev).length();
		transformProfile(*iter, path.backDir());
    };

//    std::copy(_vertices->begin(), _vertices->end(), std::ostream_iterator<osg::Vec3f>(std::cout, "\n"));

    osg::ref_ptr<osg::DrawElementsUInt> result(new osg::DrawElementsUInt(osg::PrimitiveSet::TRIANGLES, 0));

    // create indices and calculate normals for each face
    for(size_t row = 0; row < numPathVerts - 1; row++)
    {
    	for(size_t face = 0; face < numProfileVerts - 1; face++)
    	{
    		const size_t i1 = prevNumVerts + row * numProfileVerts + face;
    		const size_t i2 = i1 + 1;
    		const size_t i3 = i1 + numProfileVerts;
    		const size_t i4 = i3 + 1;

			// first triangle
			result->push_back(i1);
			result->push_back(i2);
			result->push_back(i3);

			// second triangle
			result->push_back(i2);
			result->push_back(i3);
			result->push_back(i4);

			// normal - cross product of face X and Z axis edges
			osg::Vec3f normal(-(
				(_output.vertices[i2] - _output.vertices[i1]) ^ // X edge
				(_output.vertices[i3] - _output.vertices[i1]) // Z edge;
			));

			// same normal vector for two triangles per face
			_output.normals[i1] += normal;
			_output.normals[i2] += normal;
			_output.normals[i3] += normal;
			_output.normals[i4] += normal;
    	};
    };

    for(osg::Vec3Array::iterator iter = _output.normals.begin() + prevNumVerts; iter != _output.normals.end(); iter++)
    {
    	iter->normalize();
    };

    return result;

}; // Extruder::createPrimitiveSet

void Extruder::transformProfile(const osg::Vec3& position, osg::Vec3 direction)
{
	size_t numProfileVerts = _profile.vertices.getNumElements();
    osg::Matrix transform(sptUtil::rotationMatrix(direction));

    for(size_t index = 0; index < numProfileVerts; index++)
    {
        _output.vertices.push_back(transform * (_profile.vertices[index] + _settings.vertex.offset) + position);

        osg::Vec2f texCoord(_profile.texCoords[index] + osg::Vec2(0, _state.texCoordT) + _settings.texture.offset);
        texCoord.x() *= _settings.texture.scale.x();
        texCoord.y() *= _settings.texture.scale.y();

        _output.texCoords.push_back(texCoord);
    };

};
