set(LIB_NAME sptCore)
set(HEADER_PATH ${SPT_SOURCE_DIR}/include/${LIB_NAME})

set(LIB_PUBLIC_HEADERS
    ${HEADER_PATH}/Follower.h
    ${HEADER_PATH}/Path.h
    ${HEADER_PATH}/Track.h
    ${HEADER_PATH}/TrackLocator.h
    ${HEADER_PATH}/Scenery.h
    ${HEADER_PATH}/Sector.h
    ${HEADER_PATH}/Switch.h
    ${HEADER_PATH}/SwitchableTracking.h
    ${HEADER_PATH}/SimpleTrack.h
    ${HEADER_PATH}/TrackVisitor.h)    

add_library(${LIB_NAME}
    ${LIB_PUBLIC_HEADERS}
    Follower.cpp
    Path.cpp 
    Track.cpp 
    TrackLocator.cpp
    Scenery.cpp 
    Externals.cpp
    Sector.cpp 
    Switch.cpp 
    SwitchableTracking.cpp 
    SimpleTrack.cpp
    TrackVisitor.cpp)
    
install(TARGETS ${LIB_NAME} ARCHIVE DESTINATION ${SPT_SOURCE_DIR}/lib)
