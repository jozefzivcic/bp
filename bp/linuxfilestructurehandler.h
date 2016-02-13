#ifndef FILESTRUCTUREHANDLER_H
#define FILESTRUCTUREHANDLER_H
#include "ifilestructurehandler.h"
#include <iostream>

class LinuxFileStructureHandler : public IFileStructureHandler
{
private:
    static std::string REDIRECT;
public:
    virtual bool copyDirectory(std::string source, std::string destination) override;
    virtual bool copyFile(std::string file, std::string directory) override;
    virtual bool createCopiesOfDirectory(std::string source, std::string destination, int num) override;
    virtual bool checkIfDirectoryExists(std::string directory) override;
    virtual bool controlFileStructure(std::string directory, int num) override;
};

#endif // FILESTRUCTUREHANDLER_H
