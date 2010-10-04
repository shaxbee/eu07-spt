MACRO(SETUP_PROG)
    #MESSAGE("in -->SETUP_EXE<-- ${TARGET_NAME}-->${TARGET_SRC} <--> ${TARGET_H}<--")
    ADD_EXECUTABLE(${TARGET_NAME} ${TARGET_SRC} ${TARGET_H})

    #SET_TARGET_PROPERTIES(${TARGET_NAME} PROPERTIES PROJECT_LABEL "${TARGET_LABEL}")
    SET_TARGET_PROPERTIES(${TARGET_NAME} PROPERTIES OUTPUT_NAME ${TARGET_NAME})
    SET_TARGET_PROPERTIES(${TARGET_NAME} PROPERTIES DEBUG_OUTPUT_NAME "${TARGET_NAME}${CMAKE_DEBUG_POSTFIX}")
    SET_TARGET_PROPERTIES(${TARGET_NAME} PROPERTIES RELEASE_OUTPUT_NAME "${TARGET_NAME}${CMAKE_RELEASE_POSTFIX}")
    SET_TARGET_PROPERTIES(${TARGET_NAME} PROPERTIES RELWITHDEBINFO_OUTPUT_NAME "${TARGET_NAME}${CMAKE_RELWITHDEBINFO_POSTFIX}")
    SET_TARGET_PROPERTIES(${TARGET_NAME} PROPERTIES MINSIZEREL_OUTPUT_NAME "${TARGET_NAME}${CMAKE_MINSIZEREL_POSTFIX}")
ENDMACRO(SETUP_PROG)

MACRO(LINK_INTERNAL TRGTNAME)
    FOREACH(LINKLIB ${ARGN})
        TARGET_LINK_LIBRARIES(${TRGTNAME} optimized "${LINKLIB}${CMAKE_RELEASE_POSTFIX}" debug "${LINKLIB}${CMAKE_DEBUG_POSTFIX}")
    ENDFOREACH(LINKLIB)
ENDMACRO(LINK_INTERNAL TRGTNAME)