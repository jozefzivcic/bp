#ifndef ILOGGER
#define ILOGGER
#include <iostream>

class ILogger {
public:
    virtual bool logInfo(std::string msg) = 0;
    virtual bool logWarning(std::string msg) = 0;
    virtual bool logError(std::string msg) = 0;
    virtual ~ILogger() {}
};

#endif // ILOGGER
