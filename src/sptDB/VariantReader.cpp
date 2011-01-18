#include <osgDB/ReadFile>

#include <sptDB/VariantReader.h>
#include <sptDB/BinaryReader.h>

#include <sptCore/Sector.h>

#include <boost/format.hpp>

using namespace boost;
using namespace sptDB;

namespace
{

boost::format sectorFileNameFormat("%+05d%+05d.sct");

void readSectors(BinaryReader& reader, VariantSectors& sectors, unsigned short id)
{
	uint32_t count;
	reader.read(count);

	while(count--)
	{
		int32_t x;
		reader.read(x);

		int32_t y;
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
    return boost::str(sectorFileNameFormat % (sector.x / sptCore::Sector::SIZE) % (sector.y / sptCore::Sector::SIZE));
};

std::auto_ptr<Variant> readVariant(std::istream& fin)
{
	BinaryReader reader(fin);
	reader.expectChunk("VRNT");

	reader.expectChunk("HEAD");
	reader.readVersion();

	if(reader.getVersion() < Version(1, 1))
		throw std::runtime_error("Incompatible variant file version.");

	uint16_t id;
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
