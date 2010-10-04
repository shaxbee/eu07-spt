cmake_minimum_required(VERSION 2.6)
project(spt)

enable_testing()

set(CMAKE_DEBUG_POSTFIX "d" CACHE STRING "add a postfix, usually d on windows")
set(CMAKE_RELEASE_POSTFIX "" CACHE STRING "add a postfix, usually empty on windows")
set(CMAKE_RELWITHDEBINFO_POSTFIX "rd" CACHE STRING "add a postfix, usually empty on windows")
set(CMAKE_MINSIZEREL_POSTFIX "s" CACHE STRING "add a postfix, usually empty on windows")

include(build/SptUtils.cmake)

include_directories(include)

IF(WIN32)
    include_directories(SYSTEM ${spt_SOURCE_DIR}/ext/include)
    link_directories(${spt_SOURCE_DIR}/ext/lib)
    
    #disable MSVC safety warning triggered in boost
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /wd4996")
ENDIF(WIN32)

add_subdirectory(src)
add_subdirectory(applications)
add_subdirectory(tests)
