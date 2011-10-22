include( "${wxWidgets_USE_FILE}" )

set(PYTHON_MODULE_SRC osgViewerWX.cpp)
set(PYTHON_MODULE_LIBS ${wxWidgets_LIBRARIES} osg osgViewer)
set(PYTHON_MODULE_COPY ${SPT_SOURCE_DIR}/applications/sptEditor/src/_osgwx)
    
python_module(_osgwx)
