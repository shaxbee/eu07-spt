set(LIB_NAME sptMover)

set(HEADER_PATH ${spt_SOURCE_DIR}/include/${LIB_NAME})

set(LIB_PUBLIC_HEADERS
    ${HEADER_PATH}/Vehicle.h
    ${HEADER_PATH}/Trainset.h)

add_library(${LIB_NAME}
    ${LIB_PUBLIC_HEADERS}
    Vehicle.cpp
    Trainset.cpp)

install(TARGETS ${LIB_NAME} ARCHIVE DESTINATION ${spt_SOURCE_DIR}/lib)