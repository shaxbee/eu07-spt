#ifndef SPTDB_VARIANTREADER_H
#define SPTDB_VARIANTREADER_H 1

#include <iostream>
#include <osg/Group>

namespace sptDB
{

osg::ref_ptr<osg::Group> readVariant(std::istream& fin);

}; // namespace sptDB

#endif