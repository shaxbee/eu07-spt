#include <sptCore/SwitchableTracking.h>

using namespace sptCore;

void SwitchableTracking::setPosition(const std::string& position)
{
	
	const ValidPositions& positions = getValidPositions();
	
	ValidPositions::const_iterator iter = std::find(positions.begin(), positions.end(), position);
	if(iter == positions.end())
		throw InvalidPositionException() << NameInfo(position);
	
	_position = position;
	
}; // SwitchableTracking::setPosition
