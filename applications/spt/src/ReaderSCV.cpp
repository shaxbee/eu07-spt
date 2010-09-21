#include <iostream>

#include <osgDB/Registry>
#include <osgDB/ReaderWriter>
#include <osgDB/FileNameUtils>
#include <osgDB/FileUtils>
#include <osgDB/fstream>

#include "SectorNode.h"
#include "SceneryAccess.h"

#include <sptDB/VariantReader.h>

class ReaderSCT: public osgDB::ReaderWriter
{

public:
    ReaderSCT() { }
    virtual ~ReaderSCT() { }

    virtual bool acceptsExtension(const std::string& extension) const
    {
        return osgDB::equalCaseInsensitive(extension, "scv");
    };

    virtual ReadResult readNode(const std::string& fileName, const Options* options = NULL) const
	{
		std::string ext = osgDB::getLowerCaseFileExtension(fileName);
        if(!acceptsExtension(ext)) 
			return ReadResult::FILE_NOT_HANDLED;

		std::string fullFileName = osgDB::findDataFile(fileName);
		if(fullFileName.empty())
			return ReadResult::FILE_NOT_FOUND;

		osgDB::ifstream input(fullFileName.c_str(), std::ios::binary);
        return readNode(input, options);
    }; // ReaderSCV::readNode

    virtual ReadResult readNode(std::istream& fin, const Options* options = NULL) const
    {
		try
		{
			sptCore::Sector& sector = sptDB::readSector(fin, getSceneryInstance());
			return ReadResult(new SectorNode(sector));
		}
		catch(std::exception& exc)	
		{
			osg::notify(osg::FATAL) << "Sector loading failed. " << exc.what();
		};

		return ReadResult::ERROR_IN_READING_FILE;
    };

}; // class ReaderSCV

REGISTER_OSGPLUGIN(sct, ReaderSCV)
