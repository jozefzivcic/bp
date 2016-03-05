#include "file.h"
#include <utility>

File::File(): id(0), userId(0), hash(""), name(""), fileSystemPath("") {}

File::File(const File& f) {
    id = f.id;
    userId = f.userId;
    hash = f.hash;
    name = f.name;
    fileSystemPath = f.fileSystemPath;
}

File &File::operator =(File other)
{
    swap(other);
    return *this;
}

long File::getId() const
{
    return id;
}

void File::setId(long value)
{
    id = value;
}

long File::getUserId() const
{
    return userId;
}

void File::setUserId(long value)
{
    userId = value;
}

std::string File::getHash() const
{
    return hash;
}

void File::setHash(const std::string &value)
{
    hash = value;
}

std::string File::getName() const
{
    return name;
}

void File::setName(const std::string &value)
{
    name = value;
}

std::string File::getFileSystemPath() const
{
    return fileSystemPath;
}

void File::setFileSystemPath(const std::string &value)
{
    fileSystemPath = value;
}

void File::setFile(const File &f)
{
    id = f.id;
    userId = f.userId;
    hash = f.hash;
    name = f.name;
    fileSystemPath = f.fileSystemPath;
}

void File::swap(File &f)
{
    using std::swap;
    swap(id, f.id);
    swap(userId, f.userId);
    swap(hash, f.hash);
    swap(name, f.name);
    swap(fileSystemPath, f.fileSystemPath);
}
