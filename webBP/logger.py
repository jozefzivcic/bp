import syslog


class Logger:
    def log_info(self, message):
        """
        Logs info into syslog.
        :param message: Message to be logged.
        """
        syslog.syslog(syslog.LOG_INFO, message)

    def log_warning(self, message):
        """
        Logs warning into syslog.
        :param message: Message to be logged.
        """
        syslog.syslog(syslog.LOG_WARNING, message)

    def log_error(self, message):
        """
        Logs error into syslog.
        :param message: Message to be logged.
        """
        syslog.syslog(syslog.LOG_ERR, message)

    def log_error(self, message, ex):
        """
        Logs error with exception into syslog.
        :param message: Message to be logged.
        :param ex: Exception to be logged.
        """
        s = repr(ex)
        syslog.syslog(syslog.LOG_ERR, '{0} {1}'.format(message, s))
