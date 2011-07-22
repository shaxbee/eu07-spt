#include <iostream>

#include <osg/Geode>
#include <osg/ArgumentParser>
#include <osg/Notify>

#include <osgDB/ReadFile>
#include <osgViewer/Viewer>
#include <osgViewer/ViewerEventHandlers>

#include <sptMover/Vehicle.h>

#include "SceneryAccess.h"
#include "view/VehicleView.h"

void print_vec(const osg::Vec3& vec)
{
    std::cout << vec.x() << " " << vec.y() << " " << vec.z() << std::endl;
}

int main(int argc, char** argv)
{
    osg::ArgumentParser arguments(&argc, argv);
    arguments.getApplicationUsage()->setCommandLineUsage(arguments.getApplicationName() + " scenery");

    if(arguments.argc() != 2)
    {
        arguments.getApplicationUsage()->write(std::cout);
        return 1;
    }

    std::string sceneryPath = "scenery/" + std::string(arguments[1]) + "/";
    osgDB::Registry::instance()->getDataFilePathList().push_back(sceneryPath);

    osg::ref_ptr<osg::Group> root(new osg::Group);
    osg::ref_ptr<osg::Node> scenery;

    try
    {
        scenery = osgDB::readNodeFile("default.scv");
        // if loading failed exit program
        if(!root.valid())
            return 0;
    } catch (std::exception& exc) {
        std::cout << exc.what() << std::endl;
        std::cout.flush();
        return 0;
    };

    root->addChild(scenery);

    osgViewer::Viewer viewer;

    // add stats
    viewer.addEventHandler(new osgViewer::StatsHandler());

    viewer.setSceneData(root.get());
    viewer.run();

    return 1;

}
