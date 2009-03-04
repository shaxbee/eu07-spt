#include <osg/Group>
#include <osgViewer/Viewer>

int main()
{
 
    osg::ref_ptr<osg::Group> root = new osg::Group;
    osgViewer::Viewer viewer;
    
    viewer.setSceneData(root.get());
    viewer.run();
    
    return 0;
    
}