set(LIB_NAME sptGFX)

set(HEADER_PATH ${SPT_SOURCE_DIR}/include/${LIB_NAME})

set(LIB_PUBLIC_HEADERS
    ${HEADER_PATH}/Extruder.h)
    
add_library(${LIB_NAME}
    ${LIB_PUBLIC_HEADERS}
    Extruder.cpp)

target_link_libraries(${LIB_NAME} ${OpenSceneGraph_LIBRARIES})
    
install(TARGETS ${LIB_NAME} ARCHIVE DESTINATION ${spt_SOURCE_DIR}/lib)
