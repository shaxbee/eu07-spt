#include <osgDB/ReadFile>

#include <sptDB/VariantReader.h>
#include <sptDB/BinaryReader.h>

#include <sptCore/Sector.h>

#include <sstream>

using namespace sptDB;

namespace
{

std::string getSectorFileName(unsigned int x, unsigned int y, unsigned int variantId)
{
	std::stringstream output;
	output << "scenery/test123/" << x << "_" << y;

	if(variantId)
		output << variantId;

	output << ".sct";

	return output.str();
};

}; // anonymous namespace

osg::ref_ptr<osg::Group> sptDB::readVariant(std::istream& fin)
{
	BinaryReader reader(fin);
	reader.expectChunk("VRNT");

	reader.expectChunk("HEAD");
	reader.readVersion();

	unsigned int id;
	reader.read(id);

	reader.endChunk("HEAD");

	reader.expectChunk("STLS");

	unsigned int count;
	reader.read(count);

	osg::ref_ptr<osg::Group> output = new osg::Group;
	while(count--)
	{
		unsigned int x;
		reader.read(x);

		unsigned int y;
		reader.read(y);

		output->addChild(osgDB::readNodeFile(getSectorFileName(x, y, id)));
	};

	reader.endChunk("STLS");

	reader.endChunk("VRNT");

	return output;
};