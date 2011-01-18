# add_subdirectory(components)
add_subdirectory(view)

set(TARGET_NAME spt)

set(TARGET_SRC
    main.cpp
    ReaderSCT.cpp
    ReaderSCV.cpp
    SceneryAccess.cpp
    SectorNode.cpp)
    
set(TARGET_H
    SceneryAccess.h   
    SectorNode.h)
    
setup_prog()

link_internal(${TARGET_NAME} OpenThreads osg osgDB osgViewer osgUtil osgGA)
target_link_libraries(${TARGET_NAME} sptDB sptGFX sptMover sptCore)

copy_dep(osg55 osg osgDB osgViewer osgUtil osgGA)
copy_dep(ot11 OpenThreads)

install(TARGETS ${TARGET_NAME} RUNTIME DESTINATION ${spt_SOURCE_DIR}/bin)
