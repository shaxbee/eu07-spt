#include <osgDB/ReadFile>

#include <sptDB/VariantReader.h>
#include <sptDB/BinaryReader.h>

#include <sptCore/Sector.h>

#include <boost/format.hpp>

using namespace sptDB;

namespace
{

boost::format sectorFileNameFormat("%+05d%+05d.sct");

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

		VariantSector sector = {x * sptCore::Sector::SIZE, y * sptCore::Sector::SIZE, id};
		sectors.push_back(sector);
	};
};

}; // anonymous namespace

namespace sptDB
{

std::string getSectorFileName(const VariantSector& sector)
{
	return boost::str(sectorFileNameFormat % sector.x % sector.y);
};

std::auto_ptr<Variant> readVariant(std::istream& fin)
{
	BinaryReader reader(fin);
	reader.expectChunk("VRNT");

	reader.expectChunk("HEAD");
	reader.readVersion();

	unsigned short id;
	reader.read(id);

	reader.endChunk("HEAD");

	reader.expectChunk("STLS");

	VariantSectors sectors;
	readSectors(reader, sectors, 0);
	readSectors(reader, sectors, id);

	reader.endChunk("STLS");

	reader.endChunk("VRNT");

	return std::auto_ptr<Variant>(new Variant(id, sectors));
};

};