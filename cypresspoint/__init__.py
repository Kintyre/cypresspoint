# -*- coding: utf-8 -*-

"""Top-level package for Cypress Point."""

from __future__ import unicode_literals

__author__ = """Lowell Alleman"""
__email__ = 'lowell@kintyre.co'
__version__ = '0.6.0'


def setup_logging(log_file, debug=False):
    from logging import DEBUG, INFO, Formatter, getLogger
    from logging.handlers import TimedRotatingFileHandler
    log = getLogger()
    if debug:
        log_level = DEBUG
    else:
        log_level = INFO
    log.setLevel(log_level)
    logfile = TimedRotatingFileHandler(log_file, "d", 7, backupCount=10, encoding='utf-8')
    logfile.setLevel(log_level)
    # setup log file formatting:
    logfile.setFormatter(
        Formatter('%(asctime)s [%(process)d] %(levelname)-8s %(name)s:  %(message)s'))
    log.addHandler(logfile)
    return log
