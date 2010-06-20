#ifndef SPTCORE_STATICSECTOR_H
#define SPTCORE_STATICSECTOR_H 1

namespace sptCore
{

class StaticSector: public Sector
{

public:
    template <typename RailTrackingContainerT, typename ConnectionContainerT>
    StaticSector(RailTrackingContainerT& tracking, ConnectionContainerT& connections);

    virtual const RailTracking& getNextTrack(const osg::Vec3& position, const RailTracking& from) const;
    virtual size_t getTotalTracks() const;

    virtual const Connection& getConnection(const osg::Vec3& position) const;

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
