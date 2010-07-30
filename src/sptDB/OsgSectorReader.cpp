#include <sptDB/OsgSectorReader.h>

#include <sptDB/SectorNode.h>
#include <sptDB/SectorReader.h>

using namespace sptDB;

namespace 
{
    osg::Vec3 decodeSectorPosition(const std::string& fileName)
    {
        assert(false && "Not implemented");
        return osg::Vec3();
    }; // decodeSectorPosition

    std::auto_ptr<SectorReaderCallback> getSectorReaderCallback(const osgDB::Options* options)
    {
        std::auto_ptr<SectorReaderCallback> result(NULL);

        assert(false && "Not implemented");

        return result;
    }; // getSectorReaderCallback
}; // anonymous namespace

osgDB::ReadResult OsgSectorReader::readNode(const std::string& fileName, const osgDB::Options* options) const
{
    osg::Vec3 position = decodeSectorPosition(fileName);
    std::auto_ptr<SectorReaderCallback> callback = getSectorReaderCallback(options);

    std::ifstream input(fileName, std::ios::binary);
    std::auto_ptr<Sector> sectorPtr = readSector(input, scenery, position, callback);
    Sector& sector = *sectorPtr;
    scenery.addSector(sectorPtr);

    return ReadResult(new SectorNode(sector));    
}; // sptDB::OsgSectorReader::readNode
