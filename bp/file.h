#ifndef IFILE
#define IFILE
#include <iostream>
class File {
    int _id;
    int _userId;
    std::string _hash;
    std::string _name;
    std::string _fileSystemPath;
public:
    File();
    int id() const;
    void setId(int id);
    int userId() const;
    void setUserId(int userId);
    std::string hash() const;
    void setHash(const std::string &hash);
    std::string name() const;
    void setName(const std::string &name);
    std::string fileSystemPath() const;
    void setFileSystemPath(const std::string &fileSystemPath);
};

#endif // IFILE
