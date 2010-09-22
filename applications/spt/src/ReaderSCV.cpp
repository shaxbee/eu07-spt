#include <iostream>

#include <osg/Group>
#include <osgDB/Registry>
#include <osgDB/ReaderWriter>
#include <osgDB/FileNameUtils>
#include <osgDB/FileUtils>
#include <osgDB/ReadFile>
#include <osgDB/fstream>

#include "SectorNode.h"
#include "SectorView.h"

#include <sptDB/VariantReader.h>

using namespace sptDB;

class ReaderSCV: public osgDB::ReaderWriter
{

public:
    ReaderSCV() { }
    virtual ~ReaderSCV() { }

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
		osg::ref_ptr<osg::Group> result = new osg::Group;

		try
		{
			std::auto_ptr<Variant> variant(readVariant(fin));

			for(sptDB::VariantSectors::const_iterator iter = variant->getSectors().begin(); iter != variant->getSectors().end(); iter++)
			{
				osg::ref_ptr<osg::Node> sector = osgDB::readNodeFile(getSectorFileName(*iter));
				if(sector.valid())
					result->addChild(sector);
			};

			return ReadResult(result);
		}
		catch(std::exception& exc)	
		{
			osg::notify(osg::FATAL) << "Sector loading failed. " << exc.what();
		};

		return ReadResult::ERROR_IN_READING_FILE;
    };

}; // class ReaderSCV

REGISTER_OSGPLUGIN(scv, ReaderSCV)
