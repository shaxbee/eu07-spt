#include "sptCore/SwitchableTracking.h"

#include <stdexcept>
#include <boost/format.hpp>

using boost::str;
using boost::format;

namespace sptCore
{

SwitchableTracking::SwitchableTracking(const osg::Vec2f& sector, const std::string& position):
    Track(sector), _position(position)
{
};

SwitchableTracking::~SwitchableTracking()
{
};

const std::string& SwitchableTracking::getPosition() const
{
    return _position;
}; // SwitchableTracking::getPosition    

void SwitchableTracking::setPosition(const std::string& position)
{
    if(!isValidPosition(position))
    {    
        throw std::invalid_argument(str(format("Invalid position <%s>") % position));
    }    

    _position = position;

}; // SwitchableTracking::setPosition

bool SwitchableTracking::isValidPosition(const std::string& position)
{
    auto positions(std::move(getValidPositions()));
    return std::find(positions.begin(), positions.end(), position) != positions.end();
};

}; // namespace sptCore
