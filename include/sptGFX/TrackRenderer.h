#ifndef SPTGFX_TRACKRENDERER_H
#define SPTGFX_TRACKRENDERER_H 1

#include <sptGFX/TrackRenderer.h>

namespace sptGFX
{

class TrackRenderer: public TrackRenderer
{

public:
    TrackRenderer(): _output(NULL) { }

    virtual void setOutput(osg::Geometry* output) { _output = output; }
    virtual void render(sptCore::Track* tracking, Profile* profile);

private:
    osg::ref_ptr<osg::Geometry> _output;

}; // class sptGFX::TrackRenderer

} // namespace sptGFX

#endif // header guard
