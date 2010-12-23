#ifndef SPT_VIEW_VEHICLEVIEW_H
#define SPT_VIEW_VEHICLEVIEW_H 1

#include <osg/Node>
#include <osg/Group>
#include <osg/MatrixTransform>

#include <boost/ptr_container/ptr_vector.hpp>

#include <sptMover/Vehicle.h>

namespace view
{

struct VehicleViewUpdateLevel
{
    enum UpdateLevel
    {
        NEAR = 0,
        MEDIUM = 1,
        FAR = 2,
        PASSIVE = 3
    };    
};

class VehicleViewComponent
{
public:    
    VehicleViewComponent(const sptMover::Vehicle& vehicle, std::string name, unsigned int updateLevel);
    virtual ~VehicleViewComponent() { };

    const std::string& getName() const { return _name; }
    unsigned int getUpdateLevel() const { return _updateLevel; }

    virtual void update(float time) { };
    virtual void attach(osg::Node* model) { };

protected:
    const sptMover::Vehicle& getVehicle() const { return _vehicle; }

private:
    const sptMover::Vehicle& _vehicle;
    std::string _name;
    const unsigned int _updateLevel;
};

class VehicleView: public osg::Node
{

public:
    VehicleView(sptMover::Vehicle& vehicle, osg::Node* model, unsigned int level);

    void addComponent(std::auto_ptr<VehicleViewComponent> component);
    const VehicleViewComponent& getComponent(const std::string& name) const;
    VehicleViewComponent& getComponent(const std::string& name);
    bool hasComponent(const std::string& name) const;

    virtual void traverse(osg::NodeVisitor& visitor);

    const sptMover::Vehicle& getVehicle() const { return _vehicle; };
    sptMover::Vehicle& getVehicle() { return _vehicle; };

    osg::Node* getModel() const { return _model.get(); };

    unsigned int getUpdateLevel() const { return _updateLevel; }
    void setUpdateLevel(unsigned int updateLevel) { _updateLevel = updateLevel; };
    
    void update(float time);

private:
    unsigned int _updateLevel;
    
    sptMover::Vehicle& _vehicle;
    osg::ref_ptr<osg::Node> _model;

    typedef boost::ptr_vector<VehicleViewComponent> Components;
    Components _components;

}; // class view::VehicleView

}; // namespace view

#endif // header guard
