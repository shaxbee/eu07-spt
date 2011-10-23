#set(GTEST_ROOT ${SPT_SOURCE_DIR}/ext)

set(GTEST_ONLY_STATIC TRUE)
find_package(GTest REQUIRED)

add_subdirectory(sptCore)
