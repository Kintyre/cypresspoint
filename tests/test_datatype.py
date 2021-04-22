#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
from datetime import timedelta

from cypresspoint.datatype import as_bool, reltime_to_timedelta


class TestRelativeTime(unittest.TestCase):

    def test_simple(self):
        f = reltime_to_timedelta
        td = timedelta

        self.assertEqual(f("9d"), td(days=9))
        self.assertEqual(f("2h"), td(hours=2))
        self.assertEqual(f("6m"), td(minutes=6))
        self.assertEqual(f("90s"), td(seconds=90))
        self.assertEqual(f("90"), td(seconds=90))

    @unittest.expectedFailure
    def test_combos(self):
        # These don't work either.  We don't need to support really fancy use
        # cases like this, but raise ValueError if the input isn't understood.
        f, td = reltime_to_timedelta, timedelta
        self.assertEqual(f("1d3h"), td(days=1, hours=3))
        self.assertEqual(f("2d2d"), td(days=4))

    @unittest.expectedFailure
    def test_invalid_values(self):
        # XXX: Known bug: https://github.com/Kintyre/cypresspoint/issues/1
        with self.assertRaises(ValueError):
            reltime_to_timedelta("no numbers here")

        with self.assertRaises(ValueError):
            reltime_to_timedelta("7Tb")

        with self.assertRaises(ValueError):
            reltime_to_timedelta("33 random words here")

    '''
    #
        def test_things_that_i_cant_explain(self):
            # Why is a tuple allowed here?   (not allowed explicitly in code)
            # Q:  caught by isinstance(, list) ?
    '''


class TestBoolConverter(unittest.TestCase):

    def test_bool_text(self):
        self.assertTrue(as_bool("True"))
        self.assertTrue(as_bool("true"))
        self.assertTrue(as_bool(True))
        self.assertFalse(as_bool("No"))
        self.assertFalse(as_bool(None))
