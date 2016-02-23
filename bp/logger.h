#ifndef LOGGER_H
#define LOGGER_H
#include "ilogger.h"
#include "configstorage.h"

class Logger : public ILogger
{
private:
    const ConfigStorage* storage;
public:
    virtual void logInfo(std::string msg) override;
    virtual void logWarning(std::string msg) override;
    virtual void logError(std::string msg) override;
};

#endif // LOGGER_H
