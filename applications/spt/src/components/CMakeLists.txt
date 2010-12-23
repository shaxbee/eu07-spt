set(PYTHON_MODULE_SRC 
    Bogie.cpp
    Body.cpp
    main.cpp)
set(PYTHON_MODULE_LIBS osg sptCore sptMover sptClientView)

python_module(_components)
