#ifndef IFILE
#define IFILE
#include <iostream>

/**
 * @brief The File class represents file record from database.
 */
class File {
    int id;
    int userId;
    std::string hash;
    std::string name;
    std::string fileSystemPath;
public:
    File();
    File(const File&);
    File& operator =(File other);
    /* Getters and setters */
    int getId() const;
    void setId(int value);

    int getUserId() const;
    void setUserId(int value);

    std::string getHash() const;
    void setHash(const std::string &value);

    std::string getName() const;
    void setName(const std::string &value);

    std::string getFileSystemPath() const;
    void setFileSystemPath(const std::string &value);

    /**
     * @brief setFile Sets attributes of file given as parameter according to actual object's
     * parameters.
     * @param f
     */
    void setFile(const File& f);
private:
    void swap(File& f);
};

#endif // IFILE
