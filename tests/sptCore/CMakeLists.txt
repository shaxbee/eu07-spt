set(TEST_NAME check_sptCore)
set(TEST_SRC
    Follower_t.cpp
    Path_t.cpp
    Scenery_t.cpp
    Sector_t.cpp
    Switch_t.cpp
    Track_t.cpp)

add_executable(${TEST_NAME} ${TEST_SRC})

if(UNIX)
    target_link_libraries(${TEST_NAME} pthread)
endif(UNIX)

link_internal(${TEST_NAME} osg OpenThreads)
target_link_libraries(${TEST_NAME} ${GTEST_BOTH_LIBRARIES} sptCore)

copy_dep(ot11 OpenThreads)
copy_dep(osg55 osg)

enable_testing()
gtest_add_tests(${TEST_NAME} "" ${TEST_SRC})
