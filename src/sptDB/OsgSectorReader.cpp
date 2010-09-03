#include <sptDB/OsgSectorReader.h>

#include <sptDB/SectorNode.h>
#include <sptDB/SectorReader.h>

#include <boost/lexical_cast.hpp>

using namespace sptDB;

namespace 
{
    struct SectorInfo
    {
        unsigned int variant;
        osg::Vec2 position;
    };

    SectorInfo decodeSectorName(const std::string& fileName)
    {
        SectorInfo result;

        fileName.erase(fileName.rfind("."), fileName.end());
        std::vector<std::string> fields;

        boost::split(fields, fileName, std::equals('_'));

        assert(result.size() >= 2 && "Invalid sector file name format");

        result.position = osg::Vec2(boost::lexical_cast<float>(fields[0]), boost::lexical_cast<float>(fields[1]));
        result.variant  = (fields.size() == 3) ? boost::lexical_cast<unsigned int>(fields[2]) : 0;

        return result;
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
