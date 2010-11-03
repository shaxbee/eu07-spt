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


struct RailTrackingWrapper: RailTracking, wrapper<RailTracking>
{
    RailTrackingWrapper(Sector& sector): RailTracking(sector) { }

    virtual const osg::Vec3& getExit(const osg::Vec3& entry) const { return extract<osg::Vec3&>(get_override("getExit")(entry)); }
    virtual const Path& getPath(const osg::Vec3& entry) const { return extract<const Path&>(get_override("getPath")(entry)); };
    virtual const Path& reversePath(const Path& path) const { return extract<const Path&>(get_override("reversePath")(path)); };
};

class SwitchableTrackingWrapper: public SwitchableTracking, public wrapper<SwitchableTracking>
{
public:
    SwitchableTrackingWrapper(Sector& sector): SwitchableTracking(sector) { };

    virtual const osg::Vec3& getExit(const osg::Vec3& entry) const { return extract<osg::Vec3&>(get_override("getExit")(entry)); };
    virtual const Path& getPath(const osg::Vec3& entry) const { return extract<const Path&>(get_override("getPath")(entry)); };    
    virtual const Path& reversePath(const Path& path) const { return extract<const Path&>(get_override("reversePath")(path)); };

    virtual const ValidPositions& getValidPositions() const 
    { 
        if(_initialized)
            return _positions;

        list result = extract<list>(get_override("getValidPositions")());

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

    class_<Track, bases<RailTracking>, noncopyable>("Track", no_init)
        .def("getExit", &Track::getExit, return_value_policy<return_by_value>())
        .def("getPath", &Track::getPath, return_internal_reference<>())
        .def("getDefaultPath", &Track::getDefaultPath, return_internal_reference<>());

    class_<Switch, bases<SwitchableTracking>, noncopyable>("Switch", no_init)
        .def("getExit", &Switch::getExit, return_value_policy<return_by_value>())
        .def("getPath", &Switch::getPath, return_internal_reference<>())
        .def("getStraightPath", &Switch::getStraightPath, return_internal_reference<>())
        .def("getDivertedPath", &Switch::getDivertedPath, return_internal_reference<>())
        .def("getValidPositions", &Switch::getValidPositions, return_value_policy<return_by_value>());

    class_<Scenery, noncopyable>("Scenery", no_init)
        .def("getTrack", &Scenery::getTrack, return_internal_reference<>(), args("name"))
        .def("getSwitch", &Scenery::getSwitch, return_internal_reference<>(), args("name"));
};
