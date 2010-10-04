set(LIB_NAME sptCore)
set(HEADER_PATH ${spt_SOURCE_DIR}/include/${LIB_NAME})

set(LIB_PUBLIC_HEADERS
    ${HEADER_PATH}/Follower.h
    ${HEADER_PATH}/Path.h
    ${HEADER_PATH}/RailTracking.h
    ${HEADER_PATH}/Scenery.h
    ${HEADER_PATH}/Sector.h
    ${HEADER_PATH}/Switch.h
    ${HEADER_PATH}/SwitchableTracking.h
    ${HEADER_PATH}/Track.h)    

add_library(${LIB_NAME} 
    ${LIB_PUBLIC_HEADERS}
    Follower.cpp
    Path.cpp 
    RailTracking.cpp 
    Scenery.cpp 
    Sector.cpp 
    Switch.cpp 
    SwitchableTracking.cpp 
    Track.cpp)
    
install(TARGETS ${LIB_NAME} ARCHIVE DESTINATION ${spt_SOURCE_DIR}/lib)