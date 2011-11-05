set(PYTHON_MODULE_SRC sptMover.cpp)
set(PYTHON_MODULE_LIBS sptCore sptMover osg OpenThreads)

python_module(_sptMover ../)
