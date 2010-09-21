#ifndef SPTDB_BINARY_READER
#define SPTDB_BINARY_READER 1

#include <stack>
#include <fstream>
#include <string>
#include <vector>
#include <stdexcept>

#include <boost/format.hpp>

#include <osg/Vec3f>
#include <osg/Vec3d>

namespace sptDB
{

class ChunkWatcher
{

public:
    void check(size_t bytes);
    void push(const std::string& chunk, size_t size);
    void pop(const std::string& chunk);
	const std::string& current() const;

private:
    struct Chunk
    {
        std::string name;
        size_t size;
        int left;
    };

    typedef std::stack<Chunk> ChunkStack;
    ChunkStack _chunks;
};

struct Version
{
    unsigned char major;
    unsigned char minor;
};

class BinaryReader
{
public:
    BinaryReader(std::istream& stream);

    template <typename T>
    void read(T& output);

    template <typename T>
    void read(std::vector<T>& output);

    void read(std::string& output);
    void read(osg::Vec3f& output);
    void read(osg::Vec3d& output);
    void readVersion();

    std::string readChunk();
    bool expectChunk(const std::string& type);
    void endChunk(const std::string& type);

    const Version& getVersion() const;

private:
    std::istream& _input;
    ChunkWatcher _watcher;
    Version _version;

	unsigned int _position;

    template <typename T>
    void readOsgVec(T& output);

	void checkEof(size_t bytes)
	{
		if(_input.eof())
			throw std::runtime_error(boost::str(boost::format("Unexpected file end at index %d in chunk %s") % _position % _watcher.current()));

		_position += bytes;
	};

};

template <typename T>
void BinaryReader::read(T& output)
{
    _watcher.check(sizeof(T));
    _input.read(reinterpret_cast<char*>(&output), sizeof(T));
	checkEof(sizeof(T));
};

template <typename T>
void BinaryReader::read(std::vector<T>& output)
{
    size_t count;
    read(count);

    const unsigned int elementSize = sizeof(T);

	if(!output.empty())
		throw std::runtime_error(boost::str(boost::format("Trying to write to non-empty vector in chunk %s") % _watcher.current()));

    _watcher.check(elementSize * count);

    output.reserve(count);

    while(count--)
    {
        T element;
        _input.read(reinterpret_cast<char*>(&element), elementSize);
		checkEof(elementSize);

        output.push_back(element);
    };
};

template <typename T>
void BinaryReader::readOsgVec(T& output)
{
	const size_t size = T::num_components * sizeof(typename T::value_type);
    _watcher.check(size);
    _input.read(reinterpret_cast<char*>(output.ptr()), size);
	checkEof(size);
};

}; // namespace sptDB

#endif // header guard
