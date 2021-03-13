#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import shutil
import unittest
from tempfile import mkdtemp

from cypresspoint.checkpoint import ModInputCheckpoint


class TestCheckpoint(unittest.TestCase):

    def setUp(self):
        self.test_dir = mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_simple(self):
        MY_INPUT = "my_mod_input://stanza"
        # Create (first time)
        cp = ModInputCheckpoint(self.test_dir, MY_INPUT)
        cp.load()
        last_seen = cp.get("last_seen", "DEFAULT")
        self.assertEqual(last_seen, "DEFAULT")
        cp["last_seen"] = "UPDATED-VALUE"
        self.assertEqual(cp["last_seen"], "UPDATED-VALUE")
        self.assertFalse(os.path.isfile(cp.filename))
        cp.dump()
        self.assertTrue(os.path.isfile(cp.filename))
        del cp

        # Simulate second run
        cp = ModInputCheckpoint(self.test_dir, MY_INPUT)
        cp.load()
        self.assertEqual(cp["last_seen"], "UPDATED-VALUE")
