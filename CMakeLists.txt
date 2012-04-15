cmake_minimum_required(VERSION 2.8.5)
project(SPT)

set(SPT_DEP_DIR ${SPT_SOURCE_DIR}/ext)

set(CMAKE_DEBUG_POSTFIX "d" CACHE STRING "add a postfix, usually d on windows")
set(CMAKE_RELEASE_POSTFIX "" CACHE STRING "add a postfix, usually empty on windows")
set(CMAKE_RELWITHDEBINFO_POSTFIX "rd" CACHE STRING "add a postfix, usually empty on windows")
set(CMAKE_MINSIZEREL_POSTFIX "s" CACHE STRING "add a postfix, usually empty on windows")

enable_testing()

include(cmake/SptUtils.cmake)
include(cmake/PythonUtils.cmake)

include_directories(${SPT_SOURCE_DIR}/include)

IF(WIN32)
    include_directories(SYSTEM ${SPT_DEP_DIR}/include)
    #link_directories(${SPT_DEP_DIR}/lib)
    set(BOOST_ROOT ${SPT_DEP_DIR}/boost-1.42.0)
    set(wxWidgets_ROOT_DIR ${SPT_DEP_DIR}/wxWidgets-2.8.11)
    set(ENV{OSG_DIR} ${SPT_DEP_DIR}/OpenSceneGraph-3.0.1)
    
    set(GTEST_ROOT ${SPT_DEP_DIR}/gtest-1.5.0)
    set(GTEST_MSVC_SEARCH "MD")
    
    set(CMAKE_PREFIX_PATH ${SPT_DEP_DIR})
    
    #disable MSVC safety warning triggered in boost
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /wd4996")
ENDIF(WIN32)

if(UNIX)
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -fPIC")
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -fPIC")
endif(UNIX)

find_package(Boost 1.42.0 REQUIRED python)
find_package(OpenSceneGraph 2.8.3 REQUIRED osg osgDB osgGA osgUtil osgViewer)
find_package(PythonLibs 2.7 REQUIRED)
find_package(wxWidgets 2.8.12 REQUIRED base core gl)
find_package(GTest 1.5.0 REQUIRED)

include_directories(${OPENSCENEGRAPH_INCLUDE_DIRS} ${Boost_INCLUDE_DIRS})

add_subdirectory(src)
#add_subdirectory(wrappers)
add_subdirectory(applications)
add_subdirectory(tests)

if(BUILD_OSGBOOSTPYTHON)
    add_subdirectory(ext/osgboostpython)
endif(BUILD_OSGBOOSTPYTHON)
