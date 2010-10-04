set(TARGET_NAME spt)

set(TARGET_SRC
    main.cpp
    ReaderSCT.cpp
    ReaderSCV.cpp
    SceneryAccess.cpp
    SectorNode.cpp
    SectorView.cpp
    VehicleView.cpp)
    
set(TARGET_H
    SceneryAccess.h   
    SectorNode.h    
    SectorView.h
    VehicleView.h)
    
setup_prog()

link_internal(${TARGET_NAME} OpenThreads osg osgDB osgViewer osgUtil osgGA)
target_link_libraries(${TARGET_NAME} sptDB sptGFX sptMover sptCore)

install(TARGETS ${TARGET_NAME} RUNTIME DESTINATION ${spt_SOURCE_DIR}/bin)
