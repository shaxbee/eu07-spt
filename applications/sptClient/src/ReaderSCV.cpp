#include <iostream>

#include <osg/Group>
#include <osg/MatrixTransform>

#include <osgDB/Registry>
#include <osgDB/ReaderWriter>
#include <osgDB/FileNameUtils>
#include <osgDB/FileUtils>
#include <osgDB/ReadFile>
#include <osgDB/fstream>

#include "SectorNode.h"

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
        // extract file extension and check if it is supported
        std::string ext = osgDB::getLowerCaseFileExtension(fileName);
        if(!acceptsExtension(ext))
            return ReadResult::FILE_NOT_HANDLED;

        // locate file on search path
        std::string fullFileName = osgDB::findDataFile(fileName);
        if(fullFileName.empty())
            return ReadResult::FILE_NOT_FOUND;

        // do actual read
        osgDB::ifstream input(fullFileName.c_str(), std::ios::binary);
        return readNode(input, options);
    }; // ReaderSCV::readNode

    virtual ReadResult readNode(std::istream& fin, const Options* options = NULL) const
    {
        osg::ref_ptr<osg::Group> result = new osg::Group;

        try
        {
            // read variant data from fin
            std::auto_ptr<Variant> variant(readVariant(fin));

            // for each sector
            for(sptDB::VariantSectors::const_iterator iter = variant->getSectors().begin(); iter != variant->getSectors().end(); iter++)
            {
                // read sector file
                osg::ref_ptr<osg::Node> sector = osgDB::readNodeFile(getSectorFileName(*iter));

                // if read was successful
                if(sector.valid())
                {
                    // create transform for sector
                    osg::ref_ptr<osg::MatrixTransform> transform = new osg::MatrixTransform(osg::Matrix::translate(iter->x, iter->y, 0.0f));
                    // add sector to transform
                    transform->addChild(sector.get());
                    // add transform to root
                    result->addChild(transform.get());
                }
            };

            return ReadResult(result);
        }
        catch(std::exception& exc)
        {
            // exception was catched during reading variant, report error.
            osg::notify(osg::FATAL) << "Variant loading failed. " << exc.what();
        };

        return ReadResult::ERROR_IN_READING_FILE;
    };

}; // class ReaderSCV

REGISTER_OSGPLUGIN(scv, ReaderSCV)
