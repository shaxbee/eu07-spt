#include "VehicleView.h"

#include <boost/format.hpp>
#include <boost/algorithm/string.hpp>

#include <osg/NodeVisitor>
#include <osg/NodeCallback>

#include <sptUtil/Math.h>

#include <iostream>

using namespace boost;
using namespace boost::algorithm;
using namespace sptMover;

namespace 
{

class FindNodesVisitor: public osg::NodeVisitor
{
public:
    template <typename NodeNamesT>
    FindNodesVisitor(const NodeNamesT& search):
        _search(search.begin(), search.end())
    {
        setTraversalMode(TRAVERSE_ALL_CHILDREN);
    };

    virtual void apply(osg::Node& node);

    const osg::NodeList& result() const
    {
        return _result;
    };

private:
    typedef std::set<std::string> NamesSet;
    NamesSet _search;

    std::string _search;
    osg::NodeList _result;

};

void FindNodesVisitor::apply(osg::Node& node)
{
    NamesSet::iterator iter = _search.find(to_lower_copy(node.getName()));
    if(iter != _search.end())
    {
        _search.erase(iter);
        _result.push_back(&node);
    };
    
    traverse(node);
};

class VehicleViewUpdateCallback: public osg::NodeCallback
{
public:
    VehicleViewUpdateCallback(): _lastUpdate(0.0f) { };
    
    virtual void operator()(osg::Node* node, osg::NodeVisitor* nv)
    {
        // we can use static cast because this class is placed 
        // in anonymous namespace and used only in constructor
        VehicleView* view = static_cast<VehicleView*>(node);
        
        double time = nv->getFrameStamp()->getSimulationTime();
        view->update(time - _lastUpdate);
        
        _lastUpdate = time;
    };
    
private:
    double _lastUpdate;
};
    
osg::ref_ptr<osg::MatrixTransform> makeTransform(osg::Node* root, const std::string& name)
{
    // find node with given name
    FindNodeVisitor visitor(name);
    root->accept(visitor);

    // if node was not found throw exception
    osg::Node* node = visitor.result();
    if(!node)
        return osg::ref_ptr<osg::MatrixTransform>(NULL);
//        throw std::runtime_error(str(format("Node \"%s\" not found under node \"%s\"") % name % root->getName()));

    osg::ref_ptr<osg::MatrixTransform> result = new osg::MatrixTransform;
    osg::Group* parent = node->getParent(0);

    // inject transform between node and its parent
    result->addChild(node);
    parent->replaceChild(node, result.get());

    return result;
}; // makeTransform(root, name)

}; // anonymous namespace

VehicleView::VehicleView(sptMover::Vehicle& vehicle, osg::Node* model):
    _vehicle(vehicle), _bogies(new osg::Group), _axles(new osg::Group)
{ 
    setModel(static_cast<osg::Group*>(model)); 
    setUpdateCallback(new VehicleViewUpdateCallback);
}; // VehicleView::VehicleView(vehicle, model)

void VehicleView::setModel(osg::Group* model)
{
   
    // clone model nodes (geometry remains shared)
    addChild(static_cast<osg::Node*>(model->clone(osg::CopyOp::SHALLOW_COPY)));
    
    const VehicleTraits::Bogies& bogies = _vehicle.getTraits().getBogies();

    // find and store bogie nodes
    for(size_t index=1; index <= bogies.size(); index++)
    {
        // add bogie
        osg::Node* bogie = makeTransform(this, str(format("bogie%02d") % index));
        if(!bogie)
            bogie = makeTransform(this, str(format("bogie%d") % index));
        _bogies->addChild(bogie);

        // add bogie axles
        //for(size_t axle=1; axle <= bogies[index-1].axles.size(); axle++)
        //    _axles->addChild(makeTransform(bogie, str(format("axle%02d") % axle)));
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
    setMatrix(osg::Matrix::translate((front + back) / 2));

    // update vehicle body rotation
    if(_elements & ANIMATE_BODY)
    {
        // calculate vehicle rotation
        setMatrix(getMatrix() * sptUtil::rotationMatrix(front - back));
    };

    if(_elements & ANIMATE_BOGIES)
    {
        // update bogies transform
        size_t bogie = 0;
        for(Vehicle::Followers::const_iterator iter = followers.begin(); iter != followers.end(); iter++, bogie++)
        {
            osg::MatrixTransform* transform = static_cast<osg::MatrixTransform*>(_bogies->getChild(bogie));
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
