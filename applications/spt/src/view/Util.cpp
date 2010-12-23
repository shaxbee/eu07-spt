#include <osg/NodeVisitor>
#include <view/Util.h>

namespace
{
    
class FindNodeVisitor: public osg::NodeVisitor
{
public:
    FindNodeVisitor(const std::string& search): 
        _search(search), _node(NULL) { }
    
        virtual void apply(osg::Node& node)
    {
        if(node.getName() == _search)
            _node = &node;
        else
            traverse(node);
    };
    
    osg::Node* getNode()
    {
        return _node;
    };
    
    template <typename NodeT>
    NodeT* getNodeAs()
    {
        return dynamic_cast<NodeT*>(_node);
    };
    
private:
    const std::string& _search;
    osg::Node* _node;
    
}; // ::FindNodeVisitor

}; // anonymous namespace

namespace view
{
    
osg::Node* findNode(osg::Node* root, const std::string& name)
{
    FindNodeVisitor visitor(name);
    root->accept(visitor);
    
    return visitor.getNode();
};

osg::MatrixTransform* injectTransform(osg::Node* root, const std::string& name)
{
    FindNodeVisitor visitor(name);
    root->accept(visitor);
    
    osg::Node* node = visitor.getNode();
    if(!node)
        return NULL;

    osg::ref_ptr<osg::MatrixTransform> transform = visitor.getNodeAs<osg::MatrixTransform>();
    if(transform)
        return transform;
    
    transform = new osg::MatrixTransform;
    transform->addChild(node);
    node->getParent(0)->replaceChild(node, transform);
    
    return transform.get();
};
    
}; // namespace view
    