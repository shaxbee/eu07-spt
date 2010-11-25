#ifndef SPT_VEHICLEVIEW_H
#define SPT_VEHICLEVIEW_H 1

#include <osg/Node>
#include <osg/Group>
#include <osg/MatrixTransform>

#include <sptMover/Vehicle.h>

// if distance is lower than modelLoadDistance (default: ?) then model load is requested from osgDB.
// When model is loaded setModel(model) method is called which attaches nodes to VehicleViewComponent instances.
// 
// Each VehicleViewComponent has updateLevel which defines when element will be updated. If element should be updated only on demand then PASSIVE level shall be used.
//
// There are two ways of attaching model to component:
//   * using getNodeNames() method - it must return list of node names which will be searched in model, found nodes are accessible via getNodes() method
//   * using attach(model) method - developer has to implement this method to define his custom attaching method, also useAttach method has to be defined and return true

namespace
{
    
};

class VehicleViewComponent
{
public:
    enum UpdateLevel
    {
        PASSIVE = 0,
        NEAR = 1,
        MEDIUM = 2,
        FAR = 3
    };    
    
    typedef std::vector<std::string> Names;

    VehicleViewComponent(const sptMover::Vehicle& vehicle, std::string name, UpdateLevel updateLevel);

    UpdateLevel getUpdateLevel() const { return _updateLevel; }
    virtual void update(float time) = 0;

    virtual void attach(osg::Node* model) { };
    virtual Names getNodeNames() const = 0;

    void setNodes(osg::NodeList& nodes);
    osg::NodeList& getNodes();
    const osg::NodeList& getNodes() const;

    osg::Node* getNode(std::string name)
    {
        osg::NodeList::iterator iter = std::lower_bound(_nodes.begin(), _nodes.end(), FindInNodeList(name));
        if(iter != _nodes.end() && (*iter)->getName() == name)
            return *iter;
        
        return NULL;
    }
    
private:
    const sptMover::Vehicle& vehicle;
    std::string _name;
    UpdateLevel _updateLevel;

    osg::NodeList _nodes;    
};

class VehicleView: public osg::MatrixTransform
{

public:
    VehicleView(sptMover::Vehicle& vehicle, const std::string& modelPath);

    void addComponent(std::auto_ptr<VehicleViewComponent> component);
    const VehicleViewComponent& getComponent(const std::string& name) const;
    VehicleViewComponent& getComponent(const std::string& name);
    bool hasComponent(const std::string& name) const;

    const sptMover::Vehicle& getVehicle() const { return _vehicle; };
    sptMover::Vehicle& getVehicle() { return _vehicle; }

    osg::MatrixTransform* getNode() const { return _model.get(); }
    
    void update(float time, float distance);

private:
    //! \brief Clone model and gather transforms
    void setModel(osg::Node* model);
    
    sptMover::Vehicle& _vehicle;
    std::string _modelPath;

    osg::ref_ptr<osg::MatrixTransform> _model;

}; // class spt::VehicleView

class VehicleViewParameters
{
public:
    float getModelLoadingDistance() const;

private:
    float _modelLoadingDistance;
    float _farDistance;
    float _mediumDistance;
    float _closeDistance;
};

VehicleViewParameters& getVehicleViewParameters();

#endif // header guard
