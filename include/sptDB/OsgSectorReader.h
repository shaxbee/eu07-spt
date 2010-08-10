#ifndef SPTDB_OSGSECTORREADER_H
#define SPTDB_OSGSECTORREADER_H 1

#include <osgDB/ReaderWriter>

namespace sptDB
{

class OsgSectorReader: public osgDB::ReaderWriter
{

public:
    virtual osgDB::ReadResult readNode(const std::string& fileName, const osgDB::Options* options = NULL) const; 

}; // class sptDB::OsgSectorReader

}; // namespace sptDB

#endif
