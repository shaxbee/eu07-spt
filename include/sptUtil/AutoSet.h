#ifndef SPTUTIL_AUTOSET_H
#define SPTUTIL_AUTOSET_H 1

#include <set>
#include <memory>
#include <algorithm>

#include <boost/type_traits/remove_pointer.hpp>

namespace
{

template <typename ValueT>
struct DeleteValue
{

    void operator()(const ValueT& value) { delete value; };

}; // struct ::DeleteValue

}; // anonymous namespace

namespace sptUtil
{

//! \brief Set with object lifetime management 
//!
//! Set of Value* with ownership transfered in insert and erase methods
//! \author Zbyszek "ShaXbee" Mandziejewicz
template <typename ValueT>
class AutoSet
{

public:
    typedef std::set<ValueT> InternalSetT;
    typedef std::auto_ptr<typename boost::remove_pointer<ValueT>::type> value_type;

    typedef typename InternalSetT::size_type size_type;

    typedef typename InternalSetT::iterator iterator;
    typedef typename InternalSetT::const_iterator const_iterator;

    ~AutoSet() { clear(); };

    size_type size() const { return _set.size(); }

    iterator begin() { return _set.begin(); };
    const_iterator begin() const { return _set.begin(); };

    iterator end() { return _set.end(); };
    const_iterator end() const { return _set.end(); };

    iterator find(const ValueT key) { return _set.find(key); };
    const_iterator find(const ValueT key) const { return _set.find(key); };

    //! \brief Insert value and take ownership
    //! Ownership is taken after succesfull insert
    template <typename ValueParamT>
    std::pair<iterator,bool> insert(ValueParamT& value)
    {
        std::pair<iterator,bool> result = _set.insert(value.get());

        if(result.second)
            value.release();

        return result;
    };

    void clear()
    {
        erase(begin(), end());
    };

    //! \brief Remove value at iterator position and return ownership
    //! \return auto_ptr to value
    value_type erase(iterator iter)
    {
        value_type result(*iter);
        _set.erase(iter);

        return result;
    };

    void erase(iterator start, iterator end)
    {
        std::for_each(start, end, DeleteValue<ValueT>());
        _set.erase(start, end);
    };

    //! \brief Remove value and return ownership 
    //! \return auto_ptr to value
    value_type erase(const ValueT& key)
    {
        iterator iter = _set.find(key);

        if(iter != end())
        {
            _set.erase(iter);
            return value_type(*iter);
        }

        return value_type(NULL);
    };

private:
    InternalSetT _set;

}; // sptUtil::AutoSet

}; // namespace sptUtil

#endif
