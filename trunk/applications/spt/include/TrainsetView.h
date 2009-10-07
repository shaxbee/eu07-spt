#ifndef SPT_TRAINSETVIEW_H
#define SPT_TRAINSETVIEW_H 1

namespace spt
{

class TrainsetView
{

public:
    TrainsetView(Trainset& trainset);

    void update();
//    void addVehicle(osg::Group* vehicle);

private:
    struct Geometry
    {
        osg::MatrixTransform* body;
        osg::MatrixTransform* frontBoogey;
        osg::MatrixTransform* backBoogey;
    }; // struct spt::TrainsetView::VehicleGeometry

    typedef std::vector<Geometry> Geometries;

    Trainset& _trainset;
    Geometries _geometries;

}; // class spt::TrainsetView

}; // namespace spt

#endif