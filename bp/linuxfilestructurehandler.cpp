#include "linuxfilestructurehandler.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <algorithm>
#include <iterator>
#include "fstream"
#include <iostream>
#include <dirent.h>
#include <sys/types.h>
#include <cstring>
using namespace std;

LinuxFileStructureHandler::LinuxFileStructureHandler(const ConfigStorage *s) :
    storage(s) {}

bool LinuxFileStructureHandler::copyDirectory(string source, string destination, bool copyRecursive)
{
    if (!checkIfDirectoryExists(destination))
        return false;
    DIR* directory = opendir(source.c_str());
    if (directory == NULL)
        return false;
    struct dirent entry;
    struct dirent* result;
    list<string> l;
    string newSource, newDestination;
    while(true) {
        if (readdir_r(directory, &entry, &result) != 0)
            return false;
        if (result == NULL)
            break;
        if (strcmp(entry.d_name, ".") == 0 || strcmp(entry.d_name, "..") == 0)
            continue;
        l.clear();
        l.push_back(source);
        l.push_back(entry.d_name);
        newSource = createFSPath(false, l);
        l.clear();
        l.push_back(destination);
        l.push_back(entry.d_name);
        newDestination = createFSPath(false, l);
        if (entry.d_type == DT_DIR) {
            createDirectory(newDestination);
            if (copyRecursive)
                copyDirectory(newSource, newDestination, true);
        } else {
            copyFile(newSource, destination);
            if (checkIfFileIsExecutable(newSource))
                chmod(newDestination.c_str(), S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
        }
    }
    closedir(directory);
    return true;
}

bool LinuxFileStructureHandler::copyFile(string file, string directory)
{
    ifstream inputFile(file, ios::binary);
    if (!inputFile.is_open())
        return false;
    string fileName = getFileNameFromPath(file);
    list <string> l;
    l.push_back(directory);
    l.push_back(fileName);
    string destination = createFSPath(false, l);
    ofstream output(destination, ios::binary);
    if (!output.is_open())
        return false;
    istreambuf_iterator<char> inputBegin(inputFile);
    istreambuf_iterator<char> inputEnd;
    ostreambuf_iterator<char> destinationBegin(output);
    copy(inputBegin, inputEnd, destinationBegin);
    inputFile.close();
    output.close();
    return true;
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
        if (!createDirectory(path))
            return false;
        if (!copyDirectory(source,path, true))
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

bool LinuxFileStructureHandler::controlPoolStructure(string directory, int num)
{
    if (!checkIfDirectoryExists(directory))
        return false;
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

string LinuxFileStructureHandler::createPathToNistResult(int testNum)
{
    list<string>l;
    l.push_back(".");
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

string LinuxFileStructureHandler::createPathToStoreTest(string pathToUserDirFromPool, long userId, long testId)
{
    list<string> l;
    string strUserId = to_string(userId);
    string testsRes = storage->getTestsResults();
    string strTestId = to_string(testId);
    l.push_back(pathToUserDirFromPool);
    l.push_back(strUserId);
    l.push_back(testsRes);
    l.push_back(strTestId);
    return createFSPath(true, l);
}

bool LinuxFileStructureHandler::createDirectory(string path)
{
    if (checkIfDirectoryExists(path))
        return true;
    int status = mkdir(path.c_str(), S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
    return status == 0;
}

bool LinuxFileStructureHandler::checkAndCreateUserTree(string pathToUsersDir, long userId)
{
    if (!checkIfDirectoryExists(pathToUsersDir))
        if (!createDirectory(pathToUsersDir))
            return false;
    list<string>l;
    l.push_back(pathToUsersDir);
    l.push_back(to_string(userId));
    string path = createFSPath(true, l);
    if (!checkIfDirectoryExists(path))
        if (!createDirectory(path))
            return false;
    l.push_back(storage->getTestsResults());
    path = createFSPath(true, l);
    if (!checkIfDirectoryExists(path))
        if (!createDirectory(path))
            return false;
    return true;
}

string LinuxFileStructureHandler::getFileNameFromPath(string path)
{
    size_t index = path.find_last_of('/');
    if (index == string::npos || index == path.length())
        return "";
    return path.substr(index + 1, path.length() - index - 1);
}

bool LinuxFileStructureHandler::checkIfFileIsExecutable(string file)
{

    struct stat s;
    return stat(file.c_str(), &s) == 0 && s.st_mode & S_IXUSR;
}

string LinuxFileStructureHandler::getAbsolutePath(string relativePath)
{
    char* buffer = realpath(relativePath.c_str(), NULL);
    if (buffer == NULL)
        return "";
    char* absPath = realpath(relativePath.c_str(), buffer);
    if (absPath == NULL) {
        free(buffer);
        return "";
    }
    string result(absPath);
    free(buffer);
    return result;
}
