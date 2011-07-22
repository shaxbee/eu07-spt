#include <sptCore/SwitchableTracking.h>

using namespace sptCore;

void SwitchableTracking::setPosition(const std::string& position)
{
    if(!isValidPosition(position))
        throw InvalidPositionException() << NameInfo(position);

    _position = position;

}; // SwitchableTracking::setPosition

bool SwitchableTracking::isValidPosition(const std::string& position)
{
    const ValidPositions& positions = getValidPositions();

    ValidPositions::const_iterator iter = std::find(positions.begin(), positions.end(), position);
    return iter != positions.end();
};
