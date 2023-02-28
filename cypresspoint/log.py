from __future__ import unicode_literals

import sys
from logging import Formatter, LogRecord, StreamHandler


class AlertActionFormatter(Formatter):
    """ A custom formatter for writing out Splunk's expected log messages to
    STDOUT for Modular alerts.

    Format:
        [LEVEL] [MESSAGE]
    """

    if sys.version_info < (3, 2):

        def format(self, record):
            # Python 2.7 workaround, as formatMessage() isn't used

            # type: (LogRecord) -> str
            record.message = record.getMessage()
            s = self.formatMessage(record)
            return s

    def formatMessage(self, record):
        # type: (LogRecord) -> str
        # If stack trace has already been cached (exc_text), remove it to prevent it from being written
        if hasattr(record, "exc_text") and record.exc_text:
            record.exc_text = None
        # Returns just the first line of message
        message_first_line = record.message.split("\n")[0]
        return "{} {}".format(record.levelname, message_first_line)

    def formatException(self, exec_info):
        """ Just suppress because any output here triggers a multiline event. """
        return ""


def add_simple_stderr_handler(logger, stream=None):
    handler = StreamHandler(stream)
    handler.setLevel(logger.level)
    handler.setFormatter(AlertActionFormatter())
    logger.addHandler(handler)
    return handler
