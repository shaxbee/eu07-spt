#include <iostream>

#include <osg/Geode>

#include <osg/ArgumentParser>

#include <osgDB/ReadFile>
#include <osgViewer/Viewer>
#include <osgViewer/ViewerEventHandlers>

void print_vec(const osg::Vec3& vec)
{
    std::cout << vec.x() << " " << vec.y() << " " << vec.z() << std::endl;
}
/*
osg::Geode* createAxes(osg::Geode* geode)
{

    osg::BoundingBox box = geode->getBoundingBox();
    box.expandBy(osg::BoundingBox(box.corner(0), box.corner(0) + osg::Vec3(100, 100, 100)));

    osg::Vec4 red(1.0f, 0.0f, 0.0f, 1.0f);
    osg::Vec4 green(0.0f, 1.0f, 0.0f, 1.0f);
    osg::Vec4 blue(0.0f, 0.0f, 1.0f, 1.0f);
   
    osg::Geode* result = new osg::Geode; 
    osg::Geometry* geometry = new osg::Geometry;

    osg::Vec3Array* vertices = new osg::Vec3Array;
    osg::Vec4Array* colors = new osg::Vec4Array;

    osg::Vec3Array* normals = new osg::Vec3Array;
    normals->push_back(osg::Vec3(0.0f,-1.0f,0.0f));

    // X axis
    vertices->push_back(box.corner(0));
    vertices->push_back(box.corner(1));
    colors->push_back(red);
    colors->push_back(red);

    // Y axis
    vertices->push_back(box.corner(0));
    vertices->push_back(box.corner(2));
    colors->push_back(green);
    colors->push_back(green);

    // Z axis
    vertices->push_back(box.corner(0));
    vertices->push_back(box.corner(4));
    colors->push_back(blue);
    colors->push_back(blue);

    // compose geometry
    geometry->setVertexArray(vertices);

    geometry->setColorArray(colors);
    geometry->setColorBinding(osg::Geometry::BIND_PER_VERTEX);

    geometry->setNormalArray(normals);
    geometry->setNormalBinding(osg::Geometry::BIND_OVERALL);
        
    geometry->addPrimitiveSet(new osg::DrawArrays(osg::PrimitiveSet::LINES, 0, vertices->getNumElements()));

    osg::StateSet* stateSet = new osg::StateSet;
    stateSet->setAttribute(new osg::LineWidth(3));

    result->setStateSet(stateSet);

    // add geometry to geode
    result->addDrawable(geometry);

    return result;
};
*/

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

	osg::ref_ptr<osg::Node> root;

	try
	{
		root = osgDB::readNodeFile("default.scv");
        // if loading failed exit program
		if(!root.valid())
			return 0;
	} catch (std::exception& exc) {
		std::cout << exc.what() << std::endl;
		std::cout.flush();
		return 0;
	};
//    osg::ref_ptr<osg::Geode> geode = new osg::Geode;
//    root->addChild(createAxes(geode.get()));

    osgViewer::Viewer viewer;

	// add stats
    viewer.addEventHandler(new osgViewer::StatsHandler());
    
    viewer.setSceneData(root.get());
    viewer.run();
    
    return 1;
    
}
