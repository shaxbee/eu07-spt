set(GTEST_ROOT ${spt_SOURCE_DIR}/ext)
enable_testing()

find_package(GTest REQUIRED)

add_subdirectory(sptCore)
