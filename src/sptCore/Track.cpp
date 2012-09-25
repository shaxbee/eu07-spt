#include "sptCore/Track.h"

using namespace sptCore;

Track::Track(const osg::Vec2f& sector):
	_sector(sector)
{

}

const osg::Vec2f& Track::getSector() const
{
    return _sector;
}    

Track::~Track()
{
};
