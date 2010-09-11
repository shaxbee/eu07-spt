#include <fstream>

#include <osgDB/Registry>
#include <osgDB/ReaderWriter>
#include <osgDB/FileNameUtils>

#include "SectorNode.h"
#include "SceneryAccess.h"

#include <sptDB/SceneryReader.h>

class ReaderSCT: public osgDB::ReaderWriter
{

public:
    ReaderSCT() { }
    virtual ~ReaderSCT() { }

    virtual bool acceptsExtension(const std::string& extension) const
    {
        return osgDB::equalCaseInsensitive(extension, "sct");
    };

    virtual ReadResult readNode(const std::string& fileName, const Options* options = NULL) const
    {
        std::ifstream input(fileName.c_str(), std::ios::binary);

        if(input.fail())
            return ReadResult::FILE_NOT_FOUND;

        return readNode(input, options);
    }; // sptDB::ReaderSCT::readNode

    virtual ReadResult readNode(std::istream& fin, const Options* options = NULL) const
    {
        sptCore::Sector& sector = sptDB::readSector(fin, getSceneryInstance());
        return ReadResult(new SectorNode(sector));    
    };

}; // class ReaderSCT

REGISTER_OSGPLUGIN(sct, ReaderSCT)