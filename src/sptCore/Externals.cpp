#include "sptCore/Externals.h"
#include "sptCore/Scenery.h"

#include <cmath>
#include <unordered_map>

namespace
{

std::pair<osg::Vec2f, osg::Vec3f> normalized(const osg::Vec2f& sector, const osg::Vec3f& position) 
{
    const float GRID_SIZE = 10000.0f;

    osg::Vec2f delta(
        std::floor(position.x() / GRID_SIZE) * GRID_SIZE,
        std::floor(position.y() / GRID_SIZE) * GRID_SIZE
    );    

    return 
    {
        sector + delta,
        position - osg::Vec3f(delta, 0.0f)
    };    
};

}; // anonymous namespace

namespace sptCore
{

struct ExternalsState
{
    std::unordered_map<std::pair<osg::Vec2f, osg::Vec3f>, std::pair<TrackLocator, TrackLocator>> grid;
};    

void Externals::add(const osg::Vec2f& sector, std::vector<std::pair<osg::Vec3f, TrackId>> entries)
{
    for(const auto& value: entries)
    {
        TrackLocator locator{sector, value.second};
        auto iter = _state->grid.find(normalized(sector, value.first));

        // if there is external 
        if(iter != _state->grid.end())
        {
            auto& value(iter->second);
            if(!value.second.id.isNull())
            {
                // osg::notify(osg::FATAL) << 
                //    "Duplicate external connection at <" << sector << ">, <" << value.first << ">";
                throw std::invalid_argument("Duplicate external connection");
            };
            
            value.second = locator; 
        }
        // else add open external
        else
        {
            _state->grid.insert({
                { sector, value.first }, // key
                { locator, { osg::Vec2f(), TrackId::null() } } // value
            }); 
        }
    };
};

TrackLocator Externals::getNextTrack(const osg::Vec2f& sector, const osg::Vec3f& position, const TrackId from) const
{
    auto iter = _state->grid.find(normalized(sector, position));

    if(iter != _state->grid.end())
    {
        const auto& entry = iter->second;

        if(entry.first.id == from)
        {
            return entry.second;
        }
        
        if(entry.second.id == from)
        {
            return entry.first;
        }
        
        throw std::logic_error("Invalid external connection query");    
    };

    return {osg::Vec2f(), TrackId::null()};
};    


}; // namespace sptCore;
