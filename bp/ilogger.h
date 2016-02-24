#ifndef ILOGGER
#define ILOGGER
#include <iostream>

/**
 * @brief The ILogger class loggs messages into log file.
 */
class ILogger {
public:

    /**
     * @brief logInfo Logs info message to log file.
     * @param msg Message to be logged.
     */
    virtual void logInfo(std::string msg) = 0;

    /**
     * @brief logWarning Logs warning message to log file.
     * @param msg Message to be logged.
     */
    virtual void logWarning(std::string msg) = 0;

    /**
     * @brief logError Logs error message to log file.
     * @param msg Message to be logged.
     */
    virtual void logError(std::string msg) = 0;

    /**
     * @brief ~ILogger Virtual destructor.
     */
    virtual ~ILogger() {}
};

#endif // ILOGGER
