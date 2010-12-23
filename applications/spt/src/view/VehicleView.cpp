#include "view/VehicleView.h"

#include <boost/format.hpp>
#include <boost/algorithm/string.hpp>

#include <osg/NodeVisitor>
#include <osg/NodeCallback>

#include <sptUtil/Math.h>

#include <iostream>

using namespace boost;
using namespace boost::algorithm;
using namespace sptMover;

namespace view
{

namespace 
{

class FindComponentByName
{
public:
    FindComponentByName(const std::string& name): _name(name) { };

    bool operator()(const VehicleViewComponent& component)
    {
        return component.getName() == _name;
    };

private:
    std::string _name;
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

}; // anonymous namespace

VehicleViewComponent::VehicleViewComponent(const sptMover::Vehicle& vehicle, std::string name, unsigned int updateLevel):
    _vehicle(vehicle), _name(name), _updateLevel(updateLevel) { }

VehicleView::VehicleView(sptMover::Vehicle& vehicle, osg::Node* model, unsigned int updateLevel):
    _vehicle(vehicle), 
    _model(static_cast<osg::Node*>(model->clone(osg::CopyOp::SHALLOW_COPY))), 
    _updateLevel(updateLevel)
{    
}; // VehicleView::VehicleView(vehicle, model)

void VehicleView::traverse(osg::NodeVisitor& visitor)
{
    _model->accept(visitor);
};

void VehicleView::update(float time)
{
    for(Components::iterator iter = _components.begin(); iter != _components.end(); iter++)
    {
        if(iter->getUpdateLevel() <= _updateLevel)
            iter->update(time);
    };
}; // VehicleView::update(time)

void VehicleView::addComponent(std::auto_ptr<VehicleViewComponent> component)
{
    _components.push_back(component);
};

const VehicleViewComponent& VehicleView::getComponent(const std::string& name) const
{
    Components::const_iterator iter = std::find_if(_components.begin(), _components.end(), FindComponentByName(name));
    if(iter == _components.end())
        throw std::runtime_error(str(format("Component \"%s\" not found in vehicle \"%s\"") % name % getName()));
    return *iter;
};

VehicleViewComponent& VehicleView::getComponent(const std::string& name)
{
    Components::iterator iter = std::find_if(_components.begin(), _components.end(), FindComponentByName(name));
    if(iter == _components.end())
        throw std::runtime_error(str(format("Component \"%s\" not found in vehicle \"%s\"") % name % getName()));
    return *iter;
};

bool VehicleView::hasComponent(const std::string& name) const
{
    Components::const_iterator iter = std::find_if(_components.begin(), _components.end(), FindComponentByName(name));
    return iter != _components.end();
};

}; // namespace view