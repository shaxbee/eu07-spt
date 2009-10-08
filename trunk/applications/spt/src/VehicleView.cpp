#include "VehicleView.h"

#include <sstream>

void VehicleView::setModel(osg::Group* model)
{

    _model = new osg::MatrixTransform();
    // clone model nodes (geometry remains shared)
    _model->addChild(new osg::Group(*model, osg::CopyOp::DEEP_COPY_NODES));

    // find and store boogey nodes
    for(size_t boogey=1; boogey <= _vehicle.getBoogeys().boogeys; boogey++)
    {
        std::istringstream stream("boogey");
        stream << boogey;

        _boogeys.push_back(findTransform(stream.str()));
    };

    // find and store axle nodes
    for(size_t axle=1; axle <= _vehicle.getTraits().axles; axle++)
    {
        std::istringstream stream("axle");
        stream << axle;

        _axles.push_back(findTransform(stream.str()));
    };

};