set(PYTHON_MODULE_SRC
    Decimal.cpp
    Vec3.cpp
    sptmath.cpp)
    
set(PYTHON_MODULE_HEADERS
    Decimal.h
    Vec3.h)
    
set(PYTHON_MODULE_COPY ${SPT_SOURCE_DIR}/applications/sptEditor/src/_sptmath)
    
python_module(_sptmath)
