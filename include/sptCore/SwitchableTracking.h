#ifndef SPTCORE_SWITCHABLETRACKING_H
#define SPTCORE_SWITCHABLETRACKING_H

#include <sptCore/Track.h>

#include <string>
#include <vector>

namespace sptCore
{

//! \brief Base class for tracking with switchable connections
//! \author Zbyszek "ShaXbee" Mandziejewicz
class SwitchableTracking: public Track
{

public:
    SwitchableTracking(TrackId id, const osg::Vec2f& sector, const std::string& position);
    virtual ~SwitchableTracking();

    const std::string& getPosition() const;

    //! \throw InvalidPositionException if position is not in vector of valid positions
    virtual void setPosition(const std::string& position);
    virtual bool isValidPosition(const std::string& position);

    virtual std::vector<std::string> getValidPositions() const = 0;

private:
    std::string _position;

}; // class SwitchableTracking

} // namespace sptCore

#endif // headerguard
