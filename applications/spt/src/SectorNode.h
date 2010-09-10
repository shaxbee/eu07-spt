#ifndef SECTORNODE_H
#define SECTORNODE_H 1

#include <osg/Node>
#include <osg/NodeVisitor>
#include <sptCore/Sector.h>

class SectorNode: public osg::Node
{

public:
    SectorNode(sptCore::Sector& sector);

    virtual osg::Object* cloneType() const { return NULL; } 
    virtual osg::Object* clone(const osg::CopyOp& copyop) const { return NULL; }
    virtual bool isSameKindAs(const osg::Object* obj) const { return dynamic_cast<const SectorNode*>(obj) != NULL; }
    virtual const char* className() const { return "SectorNode"; }
    virtual const char* libraryName() const { return "sptDB"; }
    virtual void accept(osg::NodeVisitor& nv) { if (nv.validNodeMask(*this)) { nv.pushOntoNodePath(this); nv.apply(*this); nv.popFromNodePath(); } }

    const sptCore::Sector& getSector() const { return _sector; }

private:
    const sptCore::Sector& _sector;

}; // class SectorNode

#endif
