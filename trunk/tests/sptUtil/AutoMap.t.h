#include <cxxtest/TestSuite.h>
#include <sptUtil/AutoMap.h>

using namespace sptUtil;

class AutoMapTestSuite: public CxxTest::TestSuite
{

public:

    struct Foo 
    { 

        static size_t count;

        static void reset() { count = 0; }

        Foo() { count++; }
        ~Foo() { count--; }

    };

    typedef AutoMap<int, Foo*> FooMap;

    void testInsert()
    {

        typedef std::pair<FooMap::iterator, bool> Result;

        FooMap map;
        Foo* foo = new Foo;
        
        {
            std::auto_ptr<Foo> fooPtr(foo);

            Result result = map.insert(1, fooPtr);
            // set.insert(foo);

            // insert should succed
            TS_ASSERT(result.second);
            // ownership must be transported
            TS_ASSERT_EQUALS(fooPtr.get(), (Foo*) NULL);
        }

        {
            std::auto_ptr<Foo> fooPtr(foo);

            // try to insert same object again
            Result result = map.insert(1, fooPtr);

            // insert should fail
            TS_ASSERT(!result.second);
            // ownership should not be transported
            TS_ASSERT_EQUALS(fooPtr.get(), foo);

            fooPtr.release();
        };

        {
            std::auto_ptr<Foo> fooPtr(new Foo);
            map.insert(2, fooPtr);

            TS_ASSERT_EQUALS(map.size(), 2);
        };

    }; // AutoMapTestSuite::testInsert

    void testErase()
    {

        FooMap map;

        Foo* foo1(new Foo);
        std::auto_ptr<Foo> fooPtr1(foo1);

        Foo* foo2(new Foo);
        std::auto_ptr<Foo> fooPtr2(foo2);

        map.insert(1, fooPtr1);
        map.insert(2, fooPtr2);

        std::auto_ptr<Foo> result(map.erase(1));
        // ownership should be transported
        TS_ASSERT_EQUALS(result.get(), foo1);
        
        map.erase(2);
        // because auto_ptr wasnt taken foo2 must be destroyed
        TS_ASSERT_EQUALS(Foo::count, 1);

        // map must be empty
        TS_ASSERT_EQUALS(map.size(), 0);

    }; // AutoMapTestSuite::testErase

    void testClear()
    {

    }; // AutoMapTestSuite::testClear

}; // class AutoMapTestSuite

size_t AutoMapTestSuite::Foo::count = 0;
