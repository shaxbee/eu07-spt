#ifndef SPTUTIL_MANAGINGMAP_H
#define SPTUTIL_MANAGINGMAP_H 1

#include <map>
#include <memory>

#include  <boost/type_traits/remove_pointer.hpp>

namespace sptUtil
{

template <typename PairT>
struct DeletePointedValue
{
	void operator()(PairT& pair) { delete pair.second; }
}; // struct ::DeleteValue

template <typename KeyT, typename ValueT>
class ManagingMap
{

public:
	typedef std::map<typename KeyT, typename ValueT> InternalMapT;
	typedef typename InternalMapT::size_type size_type;
	typedef typename InternalMapT::iterator iterator;
	typedef typename InternalMapT::const_iterator const_iterator;
	typedef typename boost::remove_pointer<typename ValueT>::type raw_data_type;

	typedef std::pair<typename KeyT, std::auto_ptr<typename raw_data_type> > value_type;

	~ManagingMap() { clear(); };

	iterator begin() { return _map.begin(); }
	const_iterator begin() const { return _map.begin(); }

	iterator end() { return _map.end(); }
	const_iterator end() const { return _map.end(); }

	iterator find(const typename KeyT& key) { return _map.find(key); };
	const_iterator find(const typename KeyT& key) const { return _map.find(key); };

	std::pair<iterator,bool> insert(value_type pair)
	{
		std::pair<iterator,bool> result = _map.insert(std::make_pair(pair.first, pair.second.get()));
		pair.second.release();
		return result;
	};

	void clear()
	{
		erase(begin(), end());
	};



    void erase(iterator pos)
	{
		delete pos->second;
		_map.erase(pos);
	};

    void erase(iterator start, iterator end)
	{
		std::for_each(start, end, DeletePointedValue<typename InternalMapT::value_type>());
		_map.erase(start, end);
	};

    size_type erase(const KeyT& key)
	{
		iterator iter = _map.find(key);
		if(iter != end())
		{
			delete iter->second;
			return 1;
		}
		else
		{
			return 0;
		};
	};

private:
	typename InternalMapT _map;

}; // class sptUtil::ManagingMap

}; // namespace sptUtil

#endif // header guard