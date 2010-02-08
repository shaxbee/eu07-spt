#ifndef SPTCORE_STATICSECTOR_H
#define SPTCORE_STATICSECTOR_H 1

namespace sptCore
{

class StaticSector: public Sector
{

public:
    StaticSector(size_t count): _count(count) { }

    virtual Track* getNextTrack(const osg::Vec3& position, Track* from) const = 0;
    virtual std::pair<Track*, Track*> getTracksAt(const osg::Vec3& position) const = 0;

    //! \brief Add track pair to sector
    //! \warning Tracks has to be added in order by position
    void add(const osg::Vec3& position, Track* first, Track* second);

    //! \brief Check correctness of data
    //!
    //! Check connections ordering, duplicates and count
    bool checkIntegrity();

private:
    typedef osg::ref_ptr<Track> TrackPtr;

    struct ConnectionsEntry
    {
        osg::Vec3 position;
        std::pair<TrackPtr, TrackPtr> tracks;
    };

    typedef std::vector<ConnectionsEntry> Connections;

    size_t _count;
    Connections _connections;

};

} // namespace sptCore

#endif // headerguard
