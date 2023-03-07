#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import unittest
from unittest.mock import MagicMock, patch

with patch.dict(sys.modules, {
    "splunk": MagicMock(),
    "splunk.persistconn": MagicMock(),
    "splunk.persistconn.application": MagicMock(),
}):

    from cypresspoint.rest_handler import RequestInfo

    class TestCheckpoint(unittest.TestCase):
        """ We can't really test much here without lots of work """

        def test_request_info(self):
            ri = RequestInfo("admin", "12345", "GET", "services/mine", {}, {})
            del ri
