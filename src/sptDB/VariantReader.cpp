#include <osgDB/ReadFile>

#include <sptDB/VariantReader.h>
#include <sptDB/BinaryReader.h>

#include <sptCore/Sector.h>

#include <boost/format.hpp>

using namespace sptDB;

namespace
{

boost::format sectorFileNameFormat("scenery/test123/%+05d%+05d.sct");

std::string getSectorFileName(int x, int y, unsigned int variantId)
{
	return boost::str(sectorFileNameFormat % x % y);
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
		int x;
		reader.read(x);

		int y;
		reader.read(y);

		output->addChild(osgDB::readNodeFile(getSectorFileName(x, y, id)));
	};

	reader.endChunk("STLS");

	reader.endChunk("VRNT");

	return output;
};