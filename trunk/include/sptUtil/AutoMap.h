#ifndef SPTUTIL_AUTOMAP_H
#define SPTUTIL_AUTOMAP_H 1

#include <map>
#include <memory>

#include  <boost/type_traits/remove_pointer.hpp>

namespace 
{

template <typename PairT>
struct DeletePointedValue
{
	void operator()(PairT& pair) { delete pair.second; }
}; // struct ::DeletePointedValue

}; // anonymous namespace

namespace sptUtil
{

template <typename KeyT, typename ValueT>
class AutoMap
{

public:
	typedef std::map<KeyT, ValueT> InternalMapT;
	typedef typename InternalMapT::size_type size_type;
	typedef typename InternalMapT::iterator iterator;
	typedef typename InternalMapT::const_iterator const_iterator;
    typedef std::auto_ptr<typename boost::remove_pointer<ValueT>::type> data_type;

    AutoMap(): _map() { };
	~AutoMap() { clear(); };

	size_type size() const { return _map.size(); };

	iterator begin() { return _map.begin(); };
	const_iterator begin() const { return _map.begin(); };

	iterator end() { return _map.end(); };
	const_iterator end() const { return _map.end(); };

	iterator find(const KeyT& key) { return _map.find(key); };
	const_iterator find(const KeyT& key) const { return _map.find(key); };

	std::pair<iterator,bool> insert(const KeyT& key, data_type& value)
	{
        value.get();
		std::pair<iterator,bool> result = _map.insert(std::make_pair(key, value.get()));

        if(result.second)
		    value.release();

		return result;
	};

	void clear()
	{
		erase(begin(), end());
	};

    data_type erase(iterator iter)
	{
        data_type result(iter->second);
		_map.erase(iter);

        return result;
	};

    void erase(iterator start, iterator end)
	{
		std::for_each(start, end, DeletePointedValue<typename InternalMapT::value_type>());
		_map.erase(start, end);
	};

    data_type erase(const KeyT& key)
	{
		iterator iter = _map.find(key);
		return iter != end() ? data_type(iter->second) : NULL;
	};

private:
	InternalMapT _map;

}; // class sptUtil::AutoMap

}; // namespace sptUtil

#endif // header guard
