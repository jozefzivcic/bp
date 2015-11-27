#include "file.h"

File::File(): _id(0), _userId(0), _hash(""), _name(""), _fileSystemPath("") {}

File::File(const File& f) {
    _id = f._id;
    _userId = f._userId;
    _hash = f._hash;
    _name = f._name;
    _fileSystemPath = f._fileSystemPath;
}

int File::userId() const
{
    return _userId;
}

void File::setUserId(int userId)
{
    _userId = userId;
}

std::string File::hash() const
{
    return _hash;
}

void File::setHash(const std::string &hash)
{
    _hash = hash;
}

std::string File::name() const
{
    return _name;
}

void File::setName(const std::string &name)
{
    _name = name;
}

std::string File::fileSystemPath() const
{
    return _fileSystemPath;
}

void File::setFileSystemPath(const std::string &fileSystemPath)
{
    _fileSystemPath = fileSystemPath;
}

void File::setFile(const File &f)
{
    _id = f._id;
    _userId = f._userId;
    _hash = f._hash;
    _name = f._name;
    _fileSystemPath = f._fileSystemPath;
}

int File::id() const
{
    return _id;
}

void File::setId(int id)
{
    _id = id;
}
