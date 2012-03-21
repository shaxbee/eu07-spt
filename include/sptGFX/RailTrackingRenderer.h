#ifndef SPTGFX_TRACKRENDERER_H
#define SPTGFX_TRACKRENDERER_H 1

#include <osg/Geometry>

#include <sptCore/Track.h>
#include <sptGFX/TrackProfile.h>

namespace sptGFX
{

//! \brief Geometry generator for Track objects
//! \author Zbyszek "ShaXbee" Mandziejewicz
class TrackRenderer
{

public:
    //! Set output for generated geometry
    virtual void setOutput(osg::Geometry* output) = 0;

    //! Render tracking to geometry
    virtual void render(sptCore::Track* tracking, TrackProfile* profile) = 0;

}; // class sptGFX::TrackRenderer    

}; // namespace sptGFX

#endif // header guard
