add_library(_sptmath SHARED
    Decimal.cpp
    Vec3.cpp
    sptmath.cpp
    Decimal.h
    Vec3.h)
    
set(PYTHON_MODULE_COPY applications/sptEditor/src/)
setup_python_module(_sptmath)
