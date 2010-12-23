set(LIB_NAME sptClientView)
set(HEADER_PATH ${SPT_SOURCE_DIR}/applications/spt/include/view)

set(LIB_PUBLIC_HEADERS
    ${HEADER_PATH}/SectorView.h
    ${HEADER_PATH}/VehicleView.h
    ${HEADER_PATH}/Util.h)    

add_library(${LIB_NAME} STATIC 
    ${LIB_PUBLIC_HEADERS}
    SectorView.cpp
    VehicleView.cpp
    Util.cpp)
    
install(TARGETS ${LIB_NAME} ARCHIVE DESTINATION ${spt_SOURCE_DIR}/lib)