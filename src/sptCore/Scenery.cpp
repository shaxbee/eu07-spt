#include "sptCore/Scenery.h"

#include "sptCore/Sector.h"
#include "sptCore/SimpleTrack.h"
#include "sptCore/SwitchableTracking.h"
#include "sptCore/Externals.h"

#include <map>
#include <unordered_map>
#include <functional>

#include <boost/format.hpp>

using boost::format;
using boost::str;

namespace sptCore
{

struct SceneryState
{
    std::map<osg::Vec2f, Sector> sectors;
    std::unordered_map<std::string, TrackLocator> aliases;
    Externals externals;

    template <typename ResultT>
    const ResultT& getAlias(const std::string& name) const;

    const Track& getTrack(const TrackLocator& locator) const;
}; // class SceneryState

const Track& SceneryState::getTrack(const TrackLocator& locator) const
{
    return sectors.at(locator.sector()).getTrack(locator.id());
}; // SceneryState::getTrack(Locator)    

template <typename ResultT>
const ResultT& SceneryState::getAlias(const std::string& name) const
{
    return dynamic_cast<const ResultT&>(getTrack(aliases.at(name)));
}; // SceneryState::getAlias

Scenery::Scenery():
    _state(new SceneryState)
{
};

Scenery::~Scenery() { };

Sector& Scenery::getSector(const osg::Vec2f& position)
{
    return _state->sectors.at(position);
}; // Scenery::getSector

const Sector& Scenery::getSector(const osg::Vec2f& position) const
{
    return _state->sectors.at(position);
}; // Scenery::getSector

bool Scenery::hasSector(const osg::Vec2f& position) const
{
    return (_state->sectors.find(position) != _state->sectors.end());
}; // Scenery::hasSector

const Track& Scenery::getNextTrack(const Track& track, const osg::Vec3f& from) const
{
    TrackId id = track.getNextTrack(from);

    if(!id)
    {
        throw std::runtime_error("Null track");
    };    

    if(!id.isExternal())
    {
        return getSector(track.getSector()).getTrack(id);
    }

    TrackLocator locator = _state->externals.getNextTrack(track.getSector(), from);
}; // Scenery::getNextTrack

const SimpleTrack& Scenery::getTrack(const std::string& name) const
{
    return _state->getAlias<SimpleTrack>(name);
}; // Scenery::getTrack

const SwitchableTracking& Scenery::getSwitch(const std::string& name) const
{
    return _state->getAlias<SwitchableTracking>(name);
}; // Scenery::getSwitch

void Scenery::addSector(Sector&& sector)
{
    auto position = sector.getPosition();
    // because of lack of .emplace method in current libstdc++ .insert has to be used
    auto result = _state->sectors.insert(std::move(std::make_pair(position, std::move(sector))));

    // if sector was not inserted
    if(!result.second)
    {    
        throw std::invalid_argument(str(format("Sector already exist at position (%f, %f)") %
                    position.x() %
                    position.y()));
    };    
}; // Scenery::addSector

void Scenery::addAliases(const osg::Vec2f& sector, Aliases&& aliases)
{
    for(const auto& entry: aliases)
    {
        _state->aliases.insert({
            entry.first,
            { sector, entry.second }
        });
    };        
};

void Scenery::addExternals(const osg::Vec2f& sector, std::vector<std::pair<osg::Vec3f, TrackId>>&& entries)
{
    _state->externals.add(sector, std::move(entries));
};

}; // namespace sptCore
