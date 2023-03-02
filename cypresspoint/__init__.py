# -*- coding: utf-8 -*-

"""Top-level package for Cypress Point."""

__author__ = """Lowell Alleman"""
__email__ = 'lowell@kintyre.co'
__version__ = '0.8.0'


def setup_logging(log_file, debug=False, formatter=None, when="midnight",
                  max_size_mb=None, backup_count=10):
    from logging import DEBUG, INFO, Formatter, getLogger
    from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
    log = getLogger()
    if debug:
        log_level = DEBUG
    else:
        log_level = INFO
    log.setLevel(log_level)

    if max_size_mb:
        logfile = RotatingFileHandler(log_file, maxBytes=max_size_mb * 1048576,
                                      backupCount=backup_count, encoding='utf-8')
    else:
        logfile = TimedRotatingFileHandler(log_file, when,
                                           backupCount=backup_count, encoding='utf-8')
    logfile.setLevel(log_level)
    # setup log file formatting:
    if formatter is None:
        formatter = Formatter('%(asctime)s [%(process)d] %(levelname)-8s %(name)s:  %(message)s')
    logfile.setFormatter(formatter)
    log.addHandler(logfile)
    return log
