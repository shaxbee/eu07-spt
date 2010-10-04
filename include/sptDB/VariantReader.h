#ifndef SPTDB_VARIANTREADER_H
#define SPTDB_VARIANTREADER_H 1

#include <iostream>
#include <algorithm>
#include <memory>

#include <osg/Group>

namespace sptDB
{

struct VariantSector
{
	int x;
	int y;
	unsigned short variantId;
};

typedef std::vector<VariantSector> VariantSectors;

class Variant
{
public:
	Variant(unsigned short variantId, VariantSectors& sectors): _variantId(variantId)
	{
		_sectors.swap(sectors);
	};

	unsigned short getVariantId() const { return _variantId; }
	const VariantSectors& getSectors() const { return _sectors; }

private:
	unsigned short _variantId;
	VariantSectors _sectors;
};

std::string getSectorFileName(const VariantSector& sector);
std::auto_ptr<Variant> readVariant(std::istream& fin);

}; // namespace sptDB

#endif
