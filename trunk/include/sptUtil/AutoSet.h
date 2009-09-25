#ifndef SPTUTIL_AUTOSET_H
#define SPTUTIL_AUTOSET_H 1

#include <set>
#include <memory>

#include  <boost/type_traits/remove_pointer.hpp>

namespace
{

template <typename ValueT>
struct DeleteValue
{

	void operator()(ValueT& value) { delete value; };

}; // struct ::DeleteValue

}; // anonymous namespace

namespace sptUtil
{

template <typename ValueT>
class AutoSet
{

public:
	typedef std::set<ValueT> InternalSetT;

	typedef typename boost::remove_pointer<ValueT>::type raw_value_type;
	typedef typename std::auto_ptr<raw_value_type> value_type;

	typedef typename InternalSetT::size_type size_type;

	typedef typename InternalSetT::iterator iterator;
	typedef typename InternalSetT::const_iterator const_iterator;

	~AutoSet() { clear(); };

	size_type size() const { return _set.size(); }

	iterator begin() { return _set.begin(); };
	const_iterator begin() const { return _set.begin(); };

	iterator end() { return _set.end(); };
	const_iterator end() const { return _set.end(); };

	iterator find(const ValueT* key) { return _set.find(key); };
	const_iterator find(const ValueT* key) const { return _set.find(key); };

	std::pair<iterator,bool> insert(value_type value)
	{
		std::pair<iterator,bool> result = _set.insert(value.get());
		value.release();
		return result;
	};

	void clear()
	{
		erase(begin(), end());
	};

    void erase(iterator pos)
	{
		delete *pos;
		_set.erase(pos);
	};

    void erase(iterator start, iterator end)
	{
		std::for_each(start, end, DeleteValue<typename ValueT>());
		_set.erase(start, end);
	};

    value_type erase(const ValueT& key)
	{
		iterator iter = _set.find(key);
		return iter != end() ? value_type(*iter) : value_type(NULL);
	};

private:
	InternalSetT _set;

}; // sptUtil::AutoSet

}; // namespace sptUtil

#endif