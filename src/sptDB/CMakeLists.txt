set(LIB_NAME sptDB)

set(HEADER_PATH ${spt_SOURCE_DIR}/include/${LIB_NAME})

set(LIB_PUBLIC_HEADERS
    ${HEADER_PATH}/BinaryReader.h
    ${HEADER_PATH}/SectorReader.h
    ${HEADER_PATH}/VariantReader.h)    

add_library(${LIB_NAME}
    ${LIB_PUBLIC_HEADERS}
    BinaryReader.cpp
    SectorReader.cpp
    VariantReader.cpp)
    
install(TARGETS ${LIB_NAME} ARCHIVE DESTINATION ${spt_SOURCE_DIR}/lib)