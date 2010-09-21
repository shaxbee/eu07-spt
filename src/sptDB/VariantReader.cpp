#include <osgDB/ReadFile>

#include <sptDB/VariantReader.h>
#include <sptDB/BinaryReader.h>

#include <sptCore/Sector.h>

#include <boost/format.hpp>

using namespace sptDB;

namespace
{

boost::format sectorFileNameFormat("%+05d%+05d.sct");

std::string getSectorFileName(int x, int y, unsigned int variantId)
{
	return boost::str(sectorFileNameFormat % x % y);
};

void readSectors(BinaryReader& reader, VariantSectors& sectors, unsigned short id)
{
	unsigned int count;
	reader.read(count);

	while(count--)
	{
		int x;
		reader.read(x);

		int y;
		reader.read(y);

		VariantSector sector = {x * Sector::SIZE, y * Sector::SIZE, id};
		sectors.push_back(sector)
	};
};

}; // anonymous namespace

std::auto_ptr<Variant> sptDB::readVariant(std::istream& fin)
{
	BinaryReader reader(fin);
	reader.expectChunk("VRNT");

	reader.expectChunk("HEAD");
	reader.readVersion();

	unsigned int id;
	reader.read(id);

	reader.endChunk("HEAD");

	reader.expectChunk("STLS");

	VariantSectors sectors;
	readSectors(reader, sectors, 0);
	readSectors(reader, sectors, id);

	reader.endChunk("STLS");

	reader.endChunk("VRNT");

	return new Variant(id, sectors);
};