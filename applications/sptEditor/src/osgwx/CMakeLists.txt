include( "${wxWidgets_USE_FILE}" )

set(PYTHON_MODULE_SRC osgViewerWX.cpp)
set(PYTHON_MODULE_LIBS ${wxWidgets_LIBRARIES} osg osgViewer)
set(PYTHON_MODULE_COPY ${SPT_SOURCE_DIR}/applications/sptEditor/src/_osgwx)
    
add_library(_osgwx osgViewerWX.cpp osgViewerWX.h)
target_link_libraries(_osgwx ${Boost_PYTHON_LIBRARY} ${PYTHON_LIBRARIES} ${wxWidgets_LIBRARIES} ${OPENSCENEGRAPH_LIBRARIES})
