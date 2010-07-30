#ifndef SPTDB_SECTORNODE_H
#define SPTDB_SECTORNODE_H 1

#include <osg/Node>
#include <sptCore/Sector>

namespace sptDB
{

class SectorNode: public osg::Node
{

public:
    SectorNode(Sector& sector);

    virtual osg::Object* cloneType() const { return NULL; } 
    virtual osg::Object* clone(const osg::CopyOp& copyop) const { return NULL; }
    virtual bool isSameKindAs(const osg::Object* obj) const { return dynamic_cast<const SectorNode*>(obj) != NULL; }
    virtual const char* className() const { return "SectorNode"; } \
    virtual const char* libraryName() const { return "sptDB"; }
    virtual void accept(osg::NodeVisitor& nv) { if (nv.validNodeMask(*this)) { nv.pushOntoNodePath(this); nv.apply(*this); nv.popFromNodePath(); } }

private:
    Sector& _sector;

}; // class sptDB::SectorNode

}; // namespace sptDB

#endif
