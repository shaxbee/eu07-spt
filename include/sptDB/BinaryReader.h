#ifndef SPTDB_BINARY_READER
#define SPTDB_BINARY_READER 1

#include <stack>
#include <fstream>
#include <string>

namespace sptDB
{

class ChunkWatcher
{

public:
    void check(size_t bytes);
    void push(const std::string& chunk, size_t size);
    void pop(const std::string& chunk);

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

class BinaryReader
{
public:
    BinaryReader(std::ifstream& stream);

    template <typename T>
    void read(T& output);

    template <typename T>
    void read(std::vector<T>& output);

    std::string& readChunk();
    bool expectChunk(const std::string& type);
    void endChunk(const std::string& type);

private:
    std::ifstream& _input;
    ChunkWatcher _watcher;

    template <typename T>
    void readOsgVec(T& output);
};

#ifdef DEBUG
    #define assert_chunk_read(bytes) _watcher.check(bytes)
#else
    #define assert_chunk_read(ignore) ((void)0)
#endif

template <typename T>
void BinaryReader::read(T& output)
{
    assert_chunk_read(sizeof(T));
    _input.read(reinterpret_cast<char*>(&output), sizeof(T));
};

template <>
void BinaryReader::read(std::string& output)
{
    size_t length;
    read(length);

    char* buffer = new char[length];

    assert_chunk_read(length);
    _input.read(buffer, length);

    output = std::string(buffer, length);
    delete[] buffer;
};

template <typename T>
void BinaryReader::read(std::vector<T>& output)
{
    size_t count;
    read(count);

    const unsigned int elementSize = sizeof(T);

    assert(output.empty() && "Trying to write to non-empty vector");
    assert_chunk_read(elementSize * count);

    output.reserve(count);

    while(count--)
    {
        T element;
        _input.read(reinterpret_cast<char*>(&element), elementSize);
        output.push_back(element);
    };
};

template <typename T>
void BinaryReader::readOsgVec(T& output)
{
    assert_chunk_read(T::num_components * sizeof(typename T::value_type));
    _input.read(reinterpret_cast<char*>(output.ptr()), T::num_components * sizeof(typename T::value_type));
};

template <>
void BinaryReader::read(osg::Vec3f& output)
{
    readOsgVec(output);
};

template <>
void BinaryReader::read(osg::Vec3d& output)
{
    readOsgVec(output);
};

}; // namespace sptDB

#endif // header guard