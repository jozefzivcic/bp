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
     * @brief createPathToNistResult Creates path to NIST tests result.
     * @param testNum Number of test in which results should be searched for.
     * @return Path to NIST test result. If testNum is not in range from 1 to 15, then returns
     * empty string.
     */
    virtual std::string createPathToNistResult(int testNum) = 0;

    /**
     * @brief getNistTestFolder Gets name of folder, which is associated with test with number
     * num.
     * @param num Number of test, which folder should be returned.
     * @return Name of folder of test num. If num is not in range from 1 to 15, then returns
     * empty string.
     */
    virtual std::string getNistTestFolder(int num) = 0;

    /**
     * @brief createPathToStoreTest Creates FS path to directory, which is created to contain
     * results from tests.
     * @param pathToUserDirFromPool Path to directory, which contains user folders.
     * @param userId Id of user to whom results are stored.
     * @param testId Id of test which will be stored.
     * @return Path to directory, where results of tests are stored.
     */
    virtual std::string createPathToStoreTest(std::string pathToUserDirFromPool, long userId, long testId) = 0;

    /**
     * @brief createDirectory Creates directory.
     * @param path New directory to be created.
     * @return True if no error occurs, false otherwise.
     */
    virtual bool createDirectory(std::string path) = 0;

    /**
     * @brief checkAndCreateUserTree Checks structure of folders in given directory for
     * given user and if some is missing creates it.
     * @param pathToUsersDir Path, where user directory should be placed.
     * @param userId Id of user, who should have directory in pathToUsersDir.
     * @return If an errors occurs false, true otherwise.
     */
    virtual bool checkAndCreateUserTree(std::string pathToUsersDir, long userId) = 0;

    /**
     * @brief ~IFileStructureHandler Virtual destructor.
     */
    virtual ~IFileStructureHandler() {}
};

#endif // IFILESTRUCTUREHANDLER

