#ifndef SPTCORE_SWITCHABLETRACKING_H
#define SPTCORE_SWITCHABLETRACKING_H

#include <sptCore/RailTracking.h>

#include <string>
#include <vector>

#include <boost/exception.hpp>

namespace sptCore
{

class SwitchableTracking: public RailTracking
{

public:
    virtual ~SwitchableTracking() { };

    std::string getPosition() const { return _position; };
    
    //! \throw InvalidPositionException if position is not in vector of valid positions
    virtual void setPosition(const std::string& position);
    
    typedef std::vector<std::string> ValidPositions;
    virtual const ValidPositions getValidPositions() const = 0;
    
    typedef boost::error_info<struct tag_name, std::string> NameInfo;
    class InvalidPositionException: public boost::exception { };

protected:
    std::string _position;

}; // class SwitchableTracking

} // namespace sptCore

#endif // headerguard
