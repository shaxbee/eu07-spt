#include <boost/python.hpp>

namespace components
{

    void export_bogie();
    void export_body();

    BOOST_PYTHON_MODULE(_components)
    {
        export_body();
        export_bogie();
    }

};