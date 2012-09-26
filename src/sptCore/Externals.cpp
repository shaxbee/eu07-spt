#include "sptCore/Externals.h"
#include "sptCore/Scenery.h"

#include <cmath>
#include <unordered_map>

namespace
{

std::pair<osg::Vec2f, osg::Vec3f> normalized(const osg::Vec2f& sector, const osg::Vec3f& position) 
{
    const float GRID_SIZE = 1000.0f;

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

// based on boost::hash_combine
template <typename T>
std::size_t hash_combine(std::size_t& seed, const T& value)
{
    std::hash<T> hasher;
    seed ^= hasher(value) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
};

}; // anonymous namespace

namespace sptCore
{

std::size_t Externals::LocationHash::operator()(const Location& value) const
{
    std::size_t result = 0;

    ::hash_combine(result, value.first.x());
    ::hash_combine(result, value.first.y());
    ::hash_combine(result, value.second.x());
    ::hash_combine(result, value.second.y());
    ::hash_combine(result, value.second.z());

    return result;
};

void Externals::add(const osg::Vec2f& sector, std::vector<std::pair<osg::Vec3f, TrackId>> entries)
{
    for(const auto& value: entries)
    {
        TrackLocator locator{sector, value.second};
        auto iter = _grid.find(normalized(sector, value.first));

        // if there is external 
        if(iter != _grid.end())
        {
            auto& value(iter->second);
            if(!value.second.id())
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
            _grid.insert({
                { sector, value.first }, // key
                { locator, { osg::Vec2f(), TrackId::null() } } // value
            }); 
        }
    };
};

TrackLocator Externals::getNextTrack(const osg::Vec2f& sector, const osg::Vec3f& position) const
{
    auto iter = _grid.find(normalized(sector, position));

    if(iter != _grid.end())
    {
        const auto& entry = iter->second;

        if(entry.first.sector() != sector)
        {
            return entry.first;
        }
        
        if(entry.second.sector() != sector)
        {
            return entry.first;
        }
        
        throw std::logic_error("Invalid external connection query");    
    };

    return {osg::Vec2f(), TrackId::null()};
};    


}; // namespace sptCore;
