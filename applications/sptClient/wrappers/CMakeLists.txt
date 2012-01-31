add_library(_view _view.cpp)
target_link_libraries(_view ${BOOST_LIBRARIES} ${BOOST_PYTHON_LIBRARIES} ${OPENSCENEGRAPH_LIBRARIES} sptCore sptMover sptClientView)

add_library(_components _components.cpp)
target_link_libraries(_view ${BOOST_LIBRARIES} ${BOOST_PYTHON_LIBRARIES} ${OPENSCENEGRAPH_LIBRARIES} sptCore sptMover sptClientView)
