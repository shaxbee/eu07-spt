#ifndef SPTCORE_SWITCHABLETRACKING_H
#define SPTCORE_SWITCHABLETRACKING_H

#include <sptCore/RailTracking.h>

#include <string>
#include <vector>

#include <boost/exception/all.hpp>

namespace sptCore
{

//! \brief Base class for tracking with switchable connections
//! \author Zbyszek "ShaXbee" Mandziejewicz
class SwitchableTracking: public RailTracking
{

public:
    SwitchableTracking(Sector& sector): RailTracking(sector) { };
    virtual ~SwitchableTracking() { };

    std::string getPosition() const { return _position; };
    
    //! \throw InvalidPositionException if position is not in vector of valid positions
    virtual void setPosition(const std::string& position);
    bool isValidPosition(const std::string& position);
    
    typedef std::vector<std::string> ValidPositions;
    virtual const ValidPositions& getValidPositions() const = 0;
    
    typedef boost::error_info<struct tag_name, std::string> NameInfo;
    class InvalidPositionException: public boost::exception { };

private:
    std::string _position;

}; // class SwitchableTracking

} // namespace sptCore

#endif // headerguard
