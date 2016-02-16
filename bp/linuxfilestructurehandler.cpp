#include "linuxfilestructurehandler.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

using namespace std;

string LinuxFileStructureHandler::REDIRECT = "> /dev/null 2>&1";

bool LinuxFileStructureHandler::copyDirectory(string source, string destination)
{
    string command = "cp -r ";
    command += source;
    command += " ";
    command += destination;
    command += " ";
    command += REDIRECT;
    int ret = system(command.c_str());
    return (ret == 0) ? true : false;
}

bool LinuxFileStructureHandler::copyFile(string file, string directory)
{
    string command = "cp ";
    command += file;
    command += " ";
    command += directory;
    command += " ";
    command += REDIRECT;
    int ret = system(command.c_str());
    return (ret == 0) ? true : false;
}

bool LinuxFileStructureHandler::createCopiesOfDirectory(string source, string destination, int num)
{
    string modifiedDestination = destination;
    if (destination[destination.length() - 1] != '/')
        modifiedDestination += "/";

    for (int i = 0; i < num; i++) {
        string path = modifiedDestination;
        path += to_string(i);
        path += "/";
        if (!copyDirectory(source,path))
            return false;
    }
    return true;
}

bool LinuxFileStructureHandler::checkIfDirectoryExists(string directory)
{
    struct stat info;
    if (stat(directory.c_str(), &info) != 0)
        return false;
    if (info.st_mode & S_IFDIR)
        return true;
    return false;
}

bool LinuxFileStructureHandler::controlFileStructure(string directory, int num)
{
    string modifiedDirectory = directory;
    if (directory[directory.length() - 1] != '/')
        modifiedDirectory += "/";
    for (int i = 0; i < num; i++) {
        string subDir = modifiedDirectory;
        subDir += to_string(i);
        if (!checkIfDirectoryExists(subDir))
            return false;
    }
    return true;
}

string LinuxFileStructureHandler::createFSPath(bool slashAtEnd, std::list<string> l)
{
    string path;
    for (string dir : l) {
        path += dir;
        if (dir[dir.length() - 1] != '/')
            path += "/";
    }
    if (!slashAtEnd)
        return path.substr(0, path.length() - 1);
    return path;
}
