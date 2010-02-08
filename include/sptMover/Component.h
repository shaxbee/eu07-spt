#ifndef SPTMOVER_COMPONENT_H
#define SPTMOVER_COMPONENT_H 1

namespace sptMover
{

class Component
{

public:
    virtual void attachModel(osg::Node* node) = 0;
    virtual void attachSound() = 0;

}; // class sptMover::Component

}; //namespace sptMover

#endif // header guard
