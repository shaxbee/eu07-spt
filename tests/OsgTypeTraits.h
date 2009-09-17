#ifndef TESTS_OSGVALUETRAITS_H
#define TESTS_OSGVALUETRAITS_H 1

#include <cxxtest/ValueTraits.h>
#include <sstream>

#include <osg/Vec3>

namespace CxxTest
{

    CXXTEST_TEMPLATE_INSTANTIATION 
    class ValueTraits<osg::Vec3>
    {

    public:
        ValueTraits(const osg::Vec3& obj)
        {
            
            std::ostringstream stream;
            stream << "osg::Vec3(x: " << obj.x() << ", y: " << obj.y() << ", z: " << obj.z() << ")";

            _output = stream.str();

        };

        const char* asString() const
        {

            return _output.c_str();

        }

    private:
        std::string _output;

    }; // class ValueTraits<osg::Vec3>

}; // namespace CxxTest

#endif // headerguard
