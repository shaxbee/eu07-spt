#include <boost/python.hpp>
#include <boost/python/stl_iterator.hpp>

#include <sptCore/Path.h>
#include <sptCore/Track.h>
#include <sptCore/Switch.h>
#include <sptCore/Sector.h>
#include <sptCore/Scenery.h>

using namespace boost;
using namespace boost::python;
using namespace sptCore;


struct TrackWrapper: public Track, public wrapper<Track>
{
    TrackWrapper(Sector& sector): Track(sector) { }

    virtual osg::Vec3 getExit(const osg::Vec3& entry) const { return get_override("getExit")(entry); }
    virtual std::auto_ptr<Path> getPath(const osg::Vec3& entry) const 
    { 
        return extract<std::auto_ptr<Path> >(get_override("getPath")(entry)); 
    };
};

class SwitchableTrackingWrapper: public SwitchableTracking, public wrapper<SwitchableTracking>
{
public:
    SwitchableTrackingWrapper(Sector& sector): SwitchableTracking(sector) { };

    virtual osg::Vec3 getExit(const osg::Vec3& entry) const { return get_override("getExit")(entry); };
    virtual std::auto_ptr<Path> getPath(const osg::Vec3& entry) const 
    { 
        return extract<std::auto_ptr<Path> >(get_override("getPath")(entry)); 
    };  

    virtual const ValidPositions& getValidPositions() const 
    { 
        if(_initialized)
            return _positions;

        list result = get_override("getValidPositions")();

        stl_input_iterator<std::string> begin(result), end;
        _positions.assign(begin, end);
        _initialized = true;

        return _positions; 
    };

    virtual void setPosition(const std::string& position) 
    { 
        override method = get_override("getValidPositions");
        if(method)
            method(position);
        else
            SwitchableTracking::setPosition(position);
    };

private:
    mutable ValidPositions _positions;
    mutable bool _initialized;
};

BOOST_PYTHON_MODULE(_sptCore)
{

    class_<Track>("Track", init<Sector&>())
        .def("getExit", &TrackWrapper::getExit);

    class_<TrackWrapper>("PyTrack", init<Sector&>())
        .def("getExit", &TrackWrapper::getExit);
//        .def("getPath", &TrackWrapper::getPath);

#if 0
    class_<SwitchableTrackingWrapper, noncopyable>("SwitchableTracking", init<Sector&>())
        .def("getExit", &SwitchableTrackingWrapper::getExit, return_value_policy<return_by_value>())
        .def("getPath", &SwitchableTrackingWrapper::getPath)
        .def("getPosition", &SwitchableTracking::getPosition)
        .def("setPosition", &SwitchableTrackingWrapper::setPosition)
        .def("isValidPosition", &SwitchableTracking::isValidPosition)
        .def("getValidPositions", &SwitchableTrackingWrapper::getValidPositions, return_value_policy<return_by_value>());

    class_<SimpleTrack, bases<Track>, noncopyable>("Track", no_init)
        .def("getExit", &SimpleTrack::getExit, return_value_policy<return_by_value>())
        .def("getPath", &SimpleTrack::getPath)
        .def("getDefaultPath", &SimpleTrack::getDefaultPath, return_internal_reference<>());

    class_<Switch, bases<SwitchableTracking>, noncopyable>("Switch", no_init)
        .def("getExit", &Switch::getExit, return_value_policy<return_by_value>())
        .def("getPath", &Switch::getPath)
        .def("getStraightPath", &Switch::getStraightPath)
        .def("getDivertedPath", &Switch::getDivertedPath)
        .def("getValidPositions", &Switch::getValidPositions, return_value_policy<return_by_value>());

    class_<Scenery, noncopyable>("Scenery", no_init)
        .def("getTrack", &Scenery::getTrack, return_internal_reference<>(), args("name"))
        .def("getSwitch", &Scenery::getSwitch, return_internal_reference<>(), args("name"));
#endif
};
