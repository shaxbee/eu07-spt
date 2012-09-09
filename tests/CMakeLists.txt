#set(GTEST_ROOT ${SPT_SOURCE_DIR}/ext)

include_directories("${SPT_SOURCE_DIR}/ext/gmock-1.6.0/include")

add_executable(trackrenderingtest trackrenderingtest.cpp)
target_link_libraries(trackrenderingtest sptGFX sptCore ${OPENSCENEGRAPH_LIBRARIES})

add_subdirectory(sptCore)
