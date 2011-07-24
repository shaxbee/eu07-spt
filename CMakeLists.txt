cmake_minimum_required(VERSION 2.6.3)
project(SPT)

option(BUILD_OSGBOOSTPYTHON "Build osg wrappers")

set(SPT_DEP_DIR ${SPT_SOURCE_DIR}/ext)

set(CMAKE_DEBUG_POSTFIX "d" CACHE STRING "add a postfix, usually d on windows")
set(CMAKE_RELEASE_POSTFIX "" CACHE STRING "add a postfix, usually empty on windows")
set(CMAKE_RELWITHDEBINFO_POSTFIX "rd" CACHE STRING "add a postfix, usually empty on windows")
set(CMAKE_MINSIZEREL_POSTFIX "s" CACHE STRING "add a postfix, usually empty on windows")

enable_testing()

include(build/SptUtils.cmake)
include(build/PythonUtils.cmake)

include_directories(include)

IF(WIN32)
    include_directories(SYSTEM ${SPT_DEP_DIR}/include)
    link_directories(${SPT_DEP_DIR}/lib)
    set(BOOST_ROOT ${SPT_DEP_DIR})
    
    set(CMAKE_PREFIX_PATH ${SPT_DEP_DIR})
    
    #disable MSVC safety warning triggered in boost
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /wd4996")
ENDIF(WIN32)

######TODO for 64 bit linux we need -fPIC probably

find_package(Boost 1.40.0 REQUIRED)
find_package(OpenSceneGraph 2.8.3 REQUIRED osgDB osgUtil osgViewer)
find_package(PythonLibs 2.7 REQUIRED)

add_subdirectory(src)
add_subdirectory(wrappers)
add_subdirectory(applications)
add_subdirectory(tests)

if(BUILD_OSGBOOSTPYTHON)
    add_subdirectory(ext/osgboostpython)
endif(BUILD_OSGBOOSTPYTHON)
