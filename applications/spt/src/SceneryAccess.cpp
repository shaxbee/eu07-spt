#include "SceneryAccess.h"

#include <sptCore/Scenery.h>

sptCore::Scenery& getSceneryInstance()
{
    static sptCore::Scenery scenery;
    return scenery;
}
