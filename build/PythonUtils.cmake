if(WIN32)
    set(Boost_USE_STATIC_LIBS OFF)
endif(WIN32)

include_directories(${PYTHON_INCLUDE_PATH})
message(${PYTHON_INCLUDE_PATH})

macro(python_module TRGTNAME)
    add_library(${TRGTNAME} SHARED ${PYTHON_MODULE_SRC} ${PYTHON_MODULE_HEADERS})
    link_internal(${TRGTNAME} ${PYTHON_MODULE_LIBS})
    target_link_libraries(${TRGTNAME} ${Boost_PYTHON_LIBRARY} ${PYTHON_LIBRARIES})
    
    set_target_properties(${TRGTNAME} PROPERTIES PREFIX "")
    if(WIN32)
        set_target_properties(${TRGTNAME} PROPERTIES SUFFIX ".pyd")
    else(WIN32)
        set_target_properties(${TRGTNAME} PROPERTIES SUFFIX ${CMAKE_SHARED_LIBRARY_SUFFIX})
    endif(WIN32)
    
    if(PYTHON_MODULE_COPY)            
        get_target_property(LIB_NAME ${TRGTNAME} LOCATION)
        get_target_property(LIB_SUFFIX ${TRGTNAME} SUFFIX)
        add_custom_command(
            TARGET ${TRGTNAME}
            POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy ${LIB_NAME} ${PYTHON_MODULE_COPY}${LIB_SUFFIX}
        )
    endif(PYTHON_MODULE_COPY)
endmacro(python_module)

macro(simple_python_module TRGTNAME)
    set(PYTHON_MODULE_SRC "${TRGTNAME}.cpp")
    set(PYTHON_MODULE_LIBS ${ARGN})
    python_module(${TRGTNAME})
endmacro(simple_python_module)
