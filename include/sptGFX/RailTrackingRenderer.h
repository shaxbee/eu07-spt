#ifndef SPTGFX_RAILTRACKINGRENDERER_H
#define SPTGFX_RAILTRACKINGRENDERER_H 1

#include <osg/Geometry>

#include <sptCore/Track.h>
#include <sptGFX/RailTrackingProfile.h>

namespace sptGFX
{

//! \brief Geometry generator for RailTracking objects
//! \author Zbyszek "ShaXbee" Mandziejewicz
class RailTrackingRenderer
{

public:
    //! Set output for generated geometry
    virtual void setOutput(osg::Geometry* output) = 0;

    //! Render tracking to geometry
    virtual void render(sptCore::RailTracking* tracking, RailTrackingProfile* profile) = 0;

}; // class sptGFX::RailTrackingRenderer    

}; // namespace sptGFX

#endif // header guard
