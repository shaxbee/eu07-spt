set(LIB_NAME sptClientView)
set(HEADER_PATH ${SPT_SOURCE_DIR}/applications/sptClient/include/view)

set(LIB_PUBLIC_HEADERS
#    ${HEADER_PATH}/SectorView.h
    ${HEADER_PATH}/VehicleView.h
    ${HEADER_PATH}/Util.h
    ${HEADER_PATH}/Components.h)

add_library(${LIB_NAME}
    ${LIB_PUBLIC_HEADERS}
#    SectorView.cpp
    VehicleView.cpp
    Util.cpp
    Components.cpp)
    
install(TARGETS ${LIB_NAME} ARCHIVE DESTINATION ${SPT_SOURCE_DIR}/applications/spt/bin)
