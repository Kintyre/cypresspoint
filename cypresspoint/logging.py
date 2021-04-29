from logging import Formatter, LogRecord


class AlertActionFormatter(Formatter):
    """ A custom formatter for writting out Splunk's expected log messages to
    STDOUT for Modular alerts.

    Format:
        [LEVEL] [MESSAGE]
    """

    def formatMessage(self, record):
        # type: (LogRecord) -> str
        # Returns just the first line of message
        mesage_first_line = record.message.split("\n")[0]
        return "{} {}".format(record.levelname, mesage_first_line)

    def formatException(self, exec_info):
        """ Just suppress because any output here triggers a multiline event. """
        return ""
