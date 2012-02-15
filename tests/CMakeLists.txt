#set(GTEST_ROOT ${SPT_SOURCE_DIR}/ext)

set(GTEST_ONLY_STATIC TRUE)
find_package(GTest REQUIRED)

add_executable(trackrenderingtest trackrenderingtest.cpp)
target_link_libraries(trackrenderingtest sptGFX sptCore ${OPENSCENEGRAPH_LIBRARIES})

add_subdirectory(sptCore)
