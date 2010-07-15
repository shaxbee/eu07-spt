#include <boost/python.hpp>

#include <sptCore/Path.h>
#include <sptCore/Track.h>
#include <sptCore/Switch.h>
#include <sptCore/Sector.h>

using namespace boost;
using namespace boost::python;
using namespace sptCore;

struct RailTrackingWrapper: RailTracking, wrapper<RailTracking>
{

public:
    RailTrackingWrapper(Sector& sector): RailTracking(sector) { }

    virtual const osg::Vec3& getExit(const osg::Vec3& entry) const { return get_override("getExit")(entry); };
    virtual const Path& getPath(const osg::Vec3& entry) const { return get_override("getPath")(entry); };
    virtual const Path& reversePath(const Path& path) const { return get_override("reversePath")(path); };

};

struct SwitchableTrackingWrapper: SwitchableTracking, wrapper<SwitchableTracking>
{
    SwitchableTrackingWrapper(Sector& sector): SwitchableTracking(sector) { };

    virtual const osg::Vec3& getExit(const osg::Vec3& entry) const { return get_override("getExit")(entry); };
    virtual const Path& getPath(const osg::Vec3& entry) const { return get_override("getPath")(entry); };    
    virtual const Path& reversePath(const Path& path) const { return get_override("reversePath")(path); };

    virtual const ValidPositions& getValidPositions() const { return get_override("getValidPositions")(); };
    virtual void setPosition(const std::string& position) 
    { 
        override method = get_override("getValidPositions");
        if(method)
            method(position);
        else
            SwitchableTracking::setPosition(position);
    };
};

BOOST_PYTHON_MODULE(sptCore)
{
    class_<Sector, noncopyable>("Sector", no_init);

    class_<RailTrackingWrapper, noncopyable>("RailTracking", init<Sector&>())
        .def("getExit", &RailTrackingWrapper::getExit, return_value_policy<return_by_value>())
        .def("getPath", &RailTrackingWrapper::getPath, return_internal_reference<>());

    class_<SwitchableTrackingWrapper, noncopyable>("SwitchableTracking", init<Sector&>())
        .def("getExit", &SwitchableTrackingWrapper::getExit, return_value_policy<return_by_value>())
        .def("getPath", &SwitchableTrackingWrapper::getPath, return_internal_reference<>())
        .def("getPosition", &SwitchableTracking::getPosition)
        .def("setPosition", &SwitchableTrackingWrapper::setPosition)
        .def("isValidPosition", &SwitchableTracking::isValidPosition)
        .def("getValidPositions", &SwitchableTrackingWrapper::getValidPositions, return_value_policy<return_by_value>());

    class_<Track, bases<RailTracking>, noncopyable >("Track", init<Sector&, std::auto_ptr<Path>& >())
        .def("getExit", &Track::getExit, return_value_policy<return_by_value>())
        .def("getPath", &Track::getPath, return_internal_reference<>())
        .def("getDefaultPath", &Track::getDefaultPath, return_internal_reference<>());

    class_<Switch, bases<SwitchableTracking>, noncopyable >("Switch", init<Sector&, std::auto_ptr<Path>&, std::auto_ptr<Path>& >())
        .def("getExit", &Switch::getExit, return_value_policy<return_by_value>())
        .def("getPath", &Switch::getPath, return_internal_reference<>())
        .def("getStraightPath", &Switch::getStraightPath, return_internal_reference<>())
        .def("getDivertedPath", &Switch::getDivertedPath, return_internal_reference<>())
        .def("getValidPositions", &Switch::getValidPositions, return_value_policy<return_by_value>());
};
