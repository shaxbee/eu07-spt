#include "VehicleView.h"

#include <boost/format.hpp>
#include <osg/NodeVisitor>
#include <osg/NodeCallback>

#include <sptUtil/Math.h>

using namespace boost;
using namespace sptMover;

namespace 
{

class FindNodeVisitor: public osg::NodeVisitor
{
public:
    FindNodeVisitor(const std::string& search): _search(search) { };

    virtual void apply(osg::Node& node)
    {
        // if node was found stop traversing
        if(node.getName() == _search)
            setTraversalMode(TRAVERSE_NONE);
        traverse(node);
    };

    osg::Node* result() const
    {
        osg::Node* node = getNodePath().back();
        return (node->getName() == _search ? node : NULL);
    };

private:
    const std::string _search;

};

class VehicleViewUpdateCallback: public osg::NodeCallback
{
public:
    virtual void operator()(osg::Node* node, osg::NodeVisitor* nv)
    {
        // we can use static cast because this class is placed 
        // in anonymous namespace and used only in constructor
        static_cast<VehicleView*>(node)->update();
    };
};
    
osg::ref_ptr<osg::MatrixTransform> makeTransform(osg::Node* root, const std::string& name)
{
    // find node with given name
    FindNodeVisitor visitor(name);
    root->accept(visitor);

    // if node was not found throw exception
    osg::Node* node = visitor.result();
    if(!node)
        throw std::runtime_error(str(format("Node \"%s\" not found under node \"%s\"") % name % root->getName()));

    osg::ref_ptr<osg::MatrixTransform> result = new osg::MatrixTransform;
    osg::Group* parent = node->getParent(0);

    // inject transform between node and its parent
    result->addChild(node);
    parent->replaceChild(node, result.get());

    return result;
}; // makeTransform(root, name)

}; // anonymous namespace

VehicleView::VehicleView(sptMover::Vehicle& vehicle, osg::Group* model):
    _vehicle(vehicle) 
{ 
    setModel(model); 
    setUpdateCallback(new VehicleViewUpdateCallback);
}; // VehicleView::VehicleView(vehicle, model)

void VehicleView::setModel(osg::Group* model)
{
    _model = new osg::MatrixTransform();
    
    // clone model nodes (geometry remains shared)
    _model->addChild(static_cast<osg::Node*>(model->clone(osg::CopyOp::SHALLOW_COPY)));
    
    const VehicleTraits::Boogeys& boogeys = _vehicle.traits.boogeys;    

    // find and store boogey nodes
    for(size_t index=1; index <= boogeys.size(); index++)
    {
        // add boogeys
        osg::Node* boogey = makeTransform(_model.get(), str(format("boogey%02d") % index));
        _boogeys->addChild(boogey);

        // add boogey axles
        for(size_t axle=1; axle <= boogeys[index-1].axles.size(); axle++)
            _axles->addChild(makeTransform(boogey, str(format("axle%02d") % axle)));
    };
};

void VehicleView::update()
{
    const Vehicle::Followers& followers = _vehicle.getFollowers();
    
    // calculate vehicle position
    // always update position because database paging 
    // needs distance from viewer to object
    osg::Vec3f front = followers.front().getPosition();
    osg::Vec3f back = followers.back().getPosition();
    _model->setMatrix(osg::Matrix::translate((front + back) / 2));

    // update vehicle body rotation
    if(_elements & ANIMATE_BODY)
    {
        // calculate vehicle rotation
        _model->setMatrix(_model->getMatrix() * sptUtil::rotationMatrix(front - back));
    };

    if(_elements & ANIMATE_BOOGEYS)
    {
        // update boogeys transform
        size_t boogey = 0;
        for(Vehicle::Followers::const_iterator iter = followers.begin(); iter != followers.end(); iter++, boogey++)
        {
            osg::MatrixTransform* transform = static_cast<osg::MatrixTransform*>(_boogeys->getChild(boogey));
            transform->setMatrix(iter->getMatrix());
        };
    };

    if(_elements & ANIMATE_AXLES)
    {
        // TODO: axles rotation
        // posible solutions: 
        //   * manualy rotating MatrixTransforms of axles
        //   * using osgAnimation and setDuration()
    };
};
