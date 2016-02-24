#ifndef LOGGER_H
#define LOGGER_H
#include "ilogger.h"
#include "configstorage.h"

/**
 * @brief The Logger class is implementation of interaface ILogger. For methods documentation
 * see the interface.
 */
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
