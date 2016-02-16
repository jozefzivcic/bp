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

string LinuxFileStructureHandler::createPathToNistResult(string testsPool, int dir, int testNum)
{
    list<string>l;
    l.push_back(testsPool);
    l.push_back(to_string(dir));
    l.push_back("experiments");
    l.push_back("AlgorithmTesting");
    l.push_back(getNistTestFolder(testNum));
    return createFSPath(true, l);
}

string LinuxFileStructureHandler::getNistTestFolder(int num)
{
    if (num < 1 || num > 15)
        return "";
    switch(num) {
    case 1:
        return "Frequency";
    case 2:
        return "BlockFrequency";
    case 3:
        return "CumulativeSums";
    case 4:
        return "Runs";
    case 5:
        return "LongestRun";
    case 6:
        return "Rank";
    case 7:
        return "FFT";
    case 8:
        return "NonOverlappingTemplate";
    case 9:
        return "OverlappingTemplate";
    case 10:
        return "Universal";
    case 11:
        return "ApproximateEntropy";
    case 12:
        return "RandomExcursions";
    case 13:
        return "RandomExcursionsVariant";
    case 14:
        return "Serial";
    case 15:
        return "LinearComplexity";
    default:
        return "";
    }
}

string LinuxFileStructureHandler::createPathToStoreTest(string pathToUserDir, long userId, long testId)
{
    list<string> l;
    l.push_back(pathToUserDir);
    l.push_back(to_string(userId));
    l.push_back(to_string(testId));
    return createFSPath(true, l);
}
