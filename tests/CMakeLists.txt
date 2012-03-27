#set(GTEST_ROOT ${SPT_SOURCE_DIR}/ext)

include_directories(${GTEST_INCLUDE_DIRS})

add_executable(trackrenderingtest trackrenderingtest.cpp)
target_link_libraries(trackrenderingtest sptGFX sptCore ${OPENSCENEGRAPH_LIBRARIES})

add_subdirectory(sptCore)