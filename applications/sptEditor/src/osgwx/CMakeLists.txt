include( "${wxWidgets_USE_FILE}" )

add_library(_osgwx SHARED osgViewerWX.cpp osgViewerWX.h)
target_link_libraries(_osgwx ${PYTHON_LIBRARIES} ${wxWidgets_LIBRARIES} ${OPENSCENEGRAPH_LIBRARIES})

set(PYTHON_MODULE_COPY applications/sptEditor/src)
setup_python_module(_osgwx)
