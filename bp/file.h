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
    File(const File&);
    /* Getters and setters */
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
    /* ----- */

    /**
     * @brief setFile Sets attributes of file given as parameter according to actual object's
     * parameters.
     * @param f
     */
    void setFile(const File& f);
};

#endif // IFILE
