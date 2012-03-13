#ifndef SECTORNODE_H
#define SECTORNODE_H 1

#include <osg/Geode>
#include <osg/NodeVisitor>
#include <sptCore/Sector.h>

class SectorNode: public osg::Node
{

public:
	SectorNode();
	SectorNode(const SectorNode& other, const osg::CopyOp& copyop = osg::CopyOp::SHALLOW_COPY);
    SectorNode(const osg::Vec3f& sector);

    virtual void traverse(osg::NodeVisitor& visitor);

    META_Node(, SectorNode);

    const sptCore::Sector& getSector() const;

private:
    const osg::Vec3f& _sector;
    osg::ref_ptr<osg::Geode> _geode;

}; // class SectorNode

#endif
