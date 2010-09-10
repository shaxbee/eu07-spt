#include "SceneryAccess.h"

#include <sptCore/Scenery.h>
#include <sptCore/Sector.h>

sptCore::Scenery& getSceneryInstance()
{
    static sptCore::Scenery scenery;
    return scenery;
}
