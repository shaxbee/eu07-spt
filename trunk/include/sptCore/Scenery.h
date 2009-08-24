class Scenery
{

public:
    virtual RailTracking* getRailTracking(const std::string& name);
    virtual Switch* getSwitch(const std::string& name);
    virtual EventedTrack* getEventedTrack(const std::string& name);

}
