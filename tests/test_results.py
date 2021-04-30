#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from cypresspoint.results import expand_vars


class TestExpandVars(unittest.TestCase):

    def test_simple_curly(self):
        style = "{}"
        out = expand_vars("hi there {name}", dict(name="bob", other="fancy"), style=style)
        self.assertEqual(out, "hi there bob")

        out = expand_vars("hi there {MISSING}", {}, style=style)
        self.assertEqual(out, "hi there ")

        out = expand_vars("test with {not a var}", {"not a var": "BLAH"}, style=style)
        self.assertEqual(out, "test with {not a var}")

        out = expand_vars(" LITERAL {} ", {}, style=style)
        self.assertEqual(out, " LITERAL {} ")

    def test_simple_curly(self):
        style = "$"
        out = expand_vars("hi there $name$", dict(name="bob", other="fancy"), style=style)
        self.assertEqual(out, "hi there bob")

        out = expand_vars("hi there $MISSING$", {}, style=style)
        self.assertEqual(out, "hi there ")

        out = expand_vars("test with $not a var$", {"not a var": "BLAH"}, style=style)
        self.assertEqual(out, "test with $not a var$")

        out = expand_vars(" LITERAL $$", {}, style=style)
        self.assertEqual(out, " LITERAL $")
