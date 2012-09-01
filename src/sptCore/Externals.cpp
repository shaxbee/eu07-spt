#include "sptCore/Externals.h"
#include "sptCore/Scenery.h"

#include <unordered_map>

namespace sptCore
{

class ExternalsImpl
{
public:
    TrackLocator getNextTrack(const TrackQuery& query) const;
    void add(const osg::Vec2f& sector, Externals::Entries entries);

private:
    std::pair<osg::Vec2f, osg::Vec3f> normalized(const osg::Vec2f& sector, const osg::Vec3f& position) const;

    typedef std::unordered_map<std::pair<osg::Vec2f, osg::Vec3f>, std::pair<TrackLocator, TrackLocator> > Grid;
    Grid _grid;

    const float GRID_SIZE;
};

std::pair<osg::Vec2f, osg::Vec3f> ExternalsImpl::normalized(const osg::Vec2f& sector, const osg::Vec3f& position) const
{
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

void ExternalsImpl::add(const osg::Vec2f& sector, Externals::Entries entries)
{
    typedef Externals::Entries::value_type value_type;

    std::for_each(entries.begin(), entries.end(), [&](const value_type& value)
    {
        TrackLocator locator{sector, value.second};
        auto iter = _grid.find(normalized(sector, value.first));

        // if there is external 
        if(iter != _grid.end())
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
            _grid.insert({
                { sector, value.first }, // key
                { locator, { osg::Vec2f(), TrackId::null() } } // value
            }); 
        }
    });
};

TrackLocator ExternalsImpl::getNextTrack(const TrackQuery& query) const
{
    auto iter = _grid.find(normalized(query.sector, query.position));

    if(iter != _grid.end())
    {
        const auto& entry = iter->second;

        if(entry.first.id == query.from)
        {
            return entry.second;
        }
        
        if(entry.second.id == query.from)
        {
            return entry.first;
        }
        
        throw std::logic_error("Invalid external connection query");    
    };

    return {osg::Vec2f(), TrackId::null()};
};    


}; // namespace sptCore;
