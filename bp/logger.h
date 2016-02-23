#ifndef LOGGER_H
#define LOGGER_H
#include "ilogger.h"
#include "configstorage.h"

class Logger : public ILogger
{
private:
    const ConfigStorage* storage;
public:
    virtual bool logInfo(std::string msg) override;
    virtual bool logWarning(std::string msg) override;
    virtual bool logError(std::string msg) override;
};

#endif // LOGGER_H
