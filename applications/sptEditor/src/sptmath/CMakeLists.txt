set(PYTHON_MODULE_SRC
    FastDec.cpp
    FastVec3.cpp
    sptmath.cpp)
    
set(PYTHON_MODULE_COPY ${SPT_SOURCE_DIR}/applications/sptEditor/src/_sptmath)
    
python_module(_sptmath)
