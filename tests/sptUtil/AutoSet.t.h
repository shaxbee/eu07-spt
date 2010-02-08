#include <cxxtest/TestSuite.h>
#include <sptUtil/AutoSet.h>

using namespace sptUtil;

struct Foo
{ 

    static size_t count;

    static void reset() { count = 0; }

    Foo() { count++; }
    ~Foo() { count--; }

};

size_t Foo::count = 0;

class AutoSetTestSuite: public CxxTest::TestSuite
{

public:

    typedef AutoSet<Foo*> FooSet;

    void testInsert()
    {

        typedef std::pair<FooSet::iterator, bool> Result;

        FooSet set;
        Foo* foo = new Foo;
        
        {
            std::auto_ptr<Foo> fooPtr(foo);

            Result result = set.insert(fooPtr);
            // set.insert(foo);

            // insert should succed
            TS_ASSERT(result.second);
            // ownership must be transported
            TS_ASSERT_EQUALS(fooPtr.get(), (Foo*) NULL);
        }

        {
            std::auto_ptr<Foo> fooPtr(foo);

            // try to insert same object again
            Result result = set.insert(fooPtr);

            // insert should fail
            TS_ASSERT(!result.second);
            // ownership should not be transported
            TS_ASSERT_EQUALS(fooPtr.get(), foo);

            fooPtr.release();
        };

        {
            std::auto_ptr<Foo> fooPtr(new Foo);
            set.insert(fooPtr);

            TS_ASSERT_EQUALS(set.size(), 2);
        };

    }; // AutoSetTestSuite::testInsert

    void testErase()
    {

        FooSet set;

        Foo* foo1(new Foo);
        std::auto_ptr<Foo> fooPtr1(foo1);

        Foo* foo2(new Foo);
        std::auto_ptr<Foo> fooPtr2(foo2);

        set.insert(fooPtr1);
        set.insert(fooPtr2);

        std::auto_ptr<Foo> result(set.erase(foo1));
        // ownership should be transported
        TS_ASSERT_EQUALS(result.get(), foo1);
        
        set.erase(foo2);
        // because auto_ptr wasnt taken foo2 must be destroyed
        TS_ASSERT_EQUALS(Foo::count, 1);

        // set must be empty
        TS_ASSERT_EQUALS(set.size(), 0);

    }; // AutoSetTestSuite::testErase

    void testClear()
    {

    }; // AutoSetTestSuite::testClear

}; // class AutoSetTestSuite
