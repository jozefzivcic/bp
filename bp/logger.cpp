#include "logger.h"
#include <syslog.h>

using namespace std;

bool Logger::logInfo(string msg)
{
    syslog(LOG_INFO, "%s", msg.c_str());
    return true;
}

bool Logger::logWarning(string msg)
{
    syslog(LOG_WARNING, "%s", msg.c_str());
    return true;
}

bool Logger::logError(string msg)
{
    syslog(LOG_ERR, "%s", msg.c_str());
    return true;
}

