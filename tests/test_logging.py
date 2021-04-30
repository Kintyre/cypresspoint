
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
from datetime import timedelta
from io import StringIO
from logging import DEBUG, INFO, Formatter, StreamHandler, getLogger
from logging.handlers import TimedRotatingFileHandler

from cypresspoint.log import AlertActionFormatter


class TestLogging(unittest.TestCase):

    def setup_logger(self, level, stream=None):
        root = getLogger()
        root.setLevel(level)
        if stream is None:
            stream = StringIO()
            self.stream = stream
        stream_handler = StreamHandler(stream)
        stream_handler.setLevel(level)
        # setup log file formatting:
        stream_handler.setFormatter(AlertActionFormatter())
        root.addHandler(stream_handler)
        return root

    def test_basic_formatting(self):
        logger = self.setup_logger(DEBUG)
        logger.error("Found half a worm in my apple")
        content = self.stream.getvalue()
        self.assertEqual(content, "ERROR Found half a worm in my apple\n")
        self.stream.seek(0)

        logger.warning("Found half a worm in my apple!")
        content = self.stream.getvalue()
        self.assertEqual(content, "WARNING Found half a worm in my apple!\n")

    def test_shorten_message(self):
        logger = self.setup_logger(DEBUG)
        logger.info("Here is a message\nthat goes across\nmultiple\nlines")
        content = self.stream.getvalue()
        self.assertEqual(content, "INFO Here is a message\n")

    def test_unhandled_exception(self):
        logger = self.setup_logger(DEBUG)
        try:
            raise ValueError("can't do it capt'n!")
        except:
            logger.exception("Enterprise down")
        content = self.stream.getvalue()
        self.assertEqual(content, "ERROR Enterprise down\n")
