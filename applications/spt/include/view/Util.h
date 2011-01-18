#include <osg/Node>
#include <osg/MatrixTransform>

namespace view
{
    
osg::Node* findNode(osg::Node* root, const std::string& name);
osg::MatrixTransform* injectTransform(osg::Node* root, const std::string& name);

}; // namespace view