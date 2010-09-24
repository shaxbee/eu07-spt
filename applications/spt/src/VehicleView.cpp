#include "VehicleView.h"

#include <boost/format.hpp>

using namespace boost;

namespace 
{
    
osg::ref_ptr<osg::MatrixTransform> makeTransform(osg::Node* root, const std::string& name)
{
    
}; // makeTransform(root, name)

}; // anonymous namespace

void VehicleView::setModel(osg::Group* model)
{
    _model = new osg::MatrixTransform();
    
    // clone model nodes (geometry remains shared)
    _model->addChild(model->clone());
    
    const VehicleTraits::Boogeys& boogeys = _vehicle.getTraits().boogeys;    

    // find and store boogey nodes
    for(size_t index=1; index <= boogeys.size(); index++)
    {
        // add boogeys
        osg::Node* boogey = makeTransform(_model.get(), str(format("boogey%02d") % index));
        _boogeys.addChild(boogey);

        // add boogey axles
        for(size_t axle=1; axle <= boogeys[index-1].axles.size(); axle++)
            _axles.addChild(makeTransform(boogey, str(format("axle%02d") % axle)));
    };
};

void VehicleView::update()
{
    const Vehicle::Followers& followers = _vehicle.getFollowers();
    
    // calculate vehicle position
    osg::Vec3f front = followers.front().getPosition();
    osg::Vec3f back = followers.back().getPosition();
    osg::Matrix transform(osg::Matrix::translate((front + back) / 2));
    
    // calculate vehicle rotation
    transform *= sptUtil::rotationMatrix(front - back);
    
    // update vehicle body transform
    _model.setMatrix(transform);    

    // update boogeys transform
    for(Vehicle::Followers::const_iterator iter = followers.begin(), size_t axle = 0; iter != followers.end(); iter++, axle++)
        _axles[axle].setMatrix(iter->getMatrix());
    
    // TODO: axles rotation
};
