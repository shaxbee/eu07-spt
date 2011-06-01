#include <view/VehicleView.h>

namespace components
{

class Body: public view::VehicleViewComponent
{
public:
    Body(const sptMover::Vehicle& vehicle, unsigned int updateLevel);

    virtual void update(float time);
    virtual void attach(osg::Node* model);

private:
    osg::ref_ptr<osg::MatrixTransform> _node;
};

class Bogie: public view::VehicleViewComponent
{
public:
    Bogie(const sptMover::Vehicle& vehicle, unsigned int index, unsigned int updateLevel);

    virtual void update(float time);
    virtual void attach(osg::Node* model);

    unsigned int getIndex() const { return _index; };

private:
    osg::ref_ptr<osg::MatrixTransform> _node;
    unsigned int _index;
    
};

}; // namespace components