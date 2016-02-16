#ifndef IFILESTRUCTUREHANDLER
#define IFILESTRUCTUREHANDLER
#include <iostream>
#include <list>

class IFileStructureHandler {
public:

    /**
     * @brief copyDirectory Copies one directory into another directory.
     * @param source Source directory to be copied.
     * @param destination Destination directory, in which the source will be copied.
     * @return If an error occurs, false, true otherwise.
     */
    virtual bool copyDirectory(std::string source, std::string destination) = 0;

    /**
     * @brief copyFile Copies file to given directory.
     * @param file File to e copied.
     * @param directory Directory, where copied file will be placed.
     * @return If an error occurs, false, true otherwise.
     */
    virtual bool copyFile(std::string file, std::string directory) = 0;

    /**
     * @brief createCopiesOfDirectory Copies source directory into destination directory num
     * times. Each copy is placed in destination/num subfolders. Subfolders are numbered
     * from 0 to num - 1.
     * @param source Source directory to be copied.
     * @param destination Destination directory, in which all subfolders will be placed.
     * @param num How many times source will be copied.
     * @return false if an error occurs during copying, or num is less than 1, true otherwise.
     */
    virtual bool createCopiesOfDirectory(std::string source, std::string destination, int num) = 0;

    /**
     * @brief checkIfDirectoryExists Checks if given directory is in file system.
     * @param directory Directory to be searched for.
     * @return True if given directory exists, false if it doesn't or process doesn't have
     * permissions to access it.
     */
    virtual bool checkIfDirectoryExists(std::string directory) = 0;

    /**
     * @brief controlFileStructure Checks if in given directory is structure needed for
     * NIST tests.
     * @param directory Directory to be searched for.
     * @param num Number of subdirectories, which should be included in directory.
     * @return true if structure is OK, else false.
     */
    virtual bool controlFileStructure(std::string directory, int num) = 0;

    /**
     * @brief createFSPath Creates filesystem path from given strings in list.
     * @param slashAtEnd If at end of path should be placed "/".
     * @param list List of directories which will be concat.
     * @return Filesystem path.
     */
    virtual std::string createFSPath(bool slashAtEnd, std::list<std::string> l) = 0;

    /**
     * @brief ~IFileStructureHandler Virtual destructor.
     */
    virtual ~IFileStructureHandler() {}
};

#endif // IFILESTRUCTUREHANDLER

