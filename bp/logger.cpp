#include "logger.h"
#include <syslog.h>

using namespace std;

void Logger::logInfo(string msg)
{
    syslog(LOG_INFO, "%s", msg.c_str());
}

void Logger::logWarning(string msg)
{
    syslog(LOG_WARNING, "%s", msg.c_str());
}

void Logger::logError(string msg)
{
    syslog(LOG_ERR, "%s", msg.c_str());
}

