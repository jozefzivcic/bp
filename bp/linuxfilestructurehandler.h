#ifndef FILESTRUCTUREHANDLER_H
#define FILESTRUCTUREHANDLER_H
#include "ifilestructurehandler.h"
#include <iostream>
#include "configstorage.h"

/**
 * @brief The LinuxFileStructureHandler class is implementation of interface
 * IFileStructureHandler. For methods documentation see base interface.
 */
class LinuxFileStructureHandler : public IFileStructureHandler
{
private:
    static std::string REDIRECT;
    const ConfigStorage* storage;
public:
    LinuxFileStructureHandler(const ConfigStorage* s);
    virtual bool copyDirectory(std::string source, std::string destination) override;
    virtual bool copyFile(std::string file, std::string directory) override;
    virtual bool createCopiesOfDirectory(std::string source, std::string destination, int num) override;
    virtual bool checkIfDirectoryExists(std::string directory) override;
    virtual bool controlPoolStructure(std::string directory, int num) override;
    virtual std::string createFSPath(bool slashAtEnd, std::list<std::string> l) override;
    virtual std::string createPathToNistResult(int testNum) override;
    virtual std::string getNistTestFolder(int num) override;
    virtual std::string createPathToStoreTest(std::string pathToUserDirFromPool, long userId, long testId) override;
    virtual bool createDirectory(std::string path) override;
    virtual bool checkAndCreateUserTree(std::string pathToUsersDir, long userId) override;
    virtual bool copyDirectoryContent(std::string source, std::string destination) override;
    virtual std::string getFileNameFromPath(std::string path) override;
};

#endif // FILESTRUCTUREHANDLER_H
