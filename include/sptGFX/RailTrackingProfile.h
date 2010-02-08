#ifndef SPTGFX_TRACKPROFILE
#define SPTGFX_TRACKPROFILE 1

namespace sptGFX
{

class TrackProfile
{

public:
    TrackProfile(osg::Geode* profile);

    virtual void render(osg::Geometry* output);
    virtual void render(osg::Geometry* output, osg::Texture2D* textureFront, osg::Texture2D* textureBack);

private:
    unsigned int getTextureUnit(osg::Geometry* geometry, osg::Texture2D* texture);

}; // class sptGFX::TrackProfile

} // namespace sptGFX

#endif // header guard
