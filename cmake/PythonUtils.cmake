if(WIN32)
    set(Boost_USE_STATIC_LIBS OFF)
endif(WIN32)

find_package(PythonLibs 2.7 REQUIRED)
include_directories(${PYTHON_INCLUDE_PATH})

macro(setup_python_module TARGET)
    target_link_libraries(${TARGET} ${PYTHON_LIBRARIES} ${Boost_PYTHON_LIBRARIES})

    set_target_properties(${TARGET} PROPERTIES PREFIX "")
    if(WIN32)
        set_target_properties(${TARGET} PROPERTIES SUFFIX ".pyd")
    endif(WIN32)

    if(PYTHON_MODULE_COPY)
        add_custom_command(
            TARGET ${TARGET}
            POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:${TARGET}> ${PROJECT_BINARY_DIR}/${PYTHON_MODULE_COPY}
        )
    endif(PYTHON_MODULE_COPY)
endmacro(setup_python_module)
