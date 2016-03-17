import syslog

class Logger:
    def log_info(self, message):
        syslog.syslog(syslog.LOG_INFO, message)

    def log_warning(self, message):
        syslog.syslog(syslog.LOG_WARNING, message)

    def log_error(self, message):
        syslog.syslog(syslog.LOG_ERR, message)

    def log_error(self, message, ex):
        s = repr(ex)
        syslog.syslog(syslog.LOG_ERR, '{0} {1}'.format(message, s))
