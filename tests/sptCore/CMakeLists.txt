set(TEST_NAME check_sptCore)
set(TEST_SRC
#    Follower_t.cpp
    Path_t.cpp
    Scenery_t.cpp
#    Sector_t.cpp
    Switch_t.cpp
    SimpleTrack_t.cpp)

add_executable(${TEST_NAME} ${TEST_SRC} ${SPT_SOURCE_DIR}/ext/gmock-1.6.0/fused-src/gmock-gtest-all.cc ${SPT_DEP_DIR}/gmock-1.6.0/fused-src/gmock_main.cc)

if(UNIX)
    target_link_libraries(${TEST_NAME} pthread)
endif(UNIX)

target_link_libraries(${TEST_NAME} ${OPENSCENEGRAPH_LIBRARIES} sptCore)

#gtest_add_tests(${TEST_NAME} "" ${TEST_SRC})
