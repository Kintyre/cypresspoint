#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest

from six import PY3, text_type

from cypresspoint.spath import splunk_dot_notation


class TestSpath(unittest.TestCase):

    def test_simple_object(self):
        test = {
            "a": 1,
            "b": 2,
        }
        output = splunk_dot_notation(test)
        self.assertEqual(output, test)

    def test_invalid_field_name(self):
        f = splunk_dot_notation
        self.assertEqual(f({"_a": 1, "b": 2}), {"a": 1, "b": 2})
        self.assertEqual(f({"$junk": "apple"}), {"junk": "apple"})
        self.assertEqual(f({"ca$h": "apple"}), {"ca_h": "apple"})

        # Make sure values are unaffected
        self.assertEqual(f({"good": "$$!CRAZY#$"}), {"good": "$$!CRAZY#$"})

    def test_invalid_values(self):
        f = splunk_dot_notation

        with self.assertRaises(TypeError):
            # Sometimes this doesn't raise an exception???
            splunk_dot_notation({"field": tuple()})

        with self.assertRaises(TypeError):
            f({"field": set()})
        with self.assertRaises(TypeError):
            f({"field": object()})
        with self.assertRaises(TypeError):
            f({"field": object})

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            splunk_dot_notation([{"a": 1}, {"a": 2}])

    '''
    #@unittest.expectedFailure
        def test_things_that_i_cant_explain(self):
            # Why is a tuple allowed here?   (not allowed explicitly in code)
            # Q:  caught by isinstance(, list) ?
    '''

    def test_unicode(self):
        # Reproduce bug found between Python 2 vs 3
        splunk_dot_notation({"a": text_type("value")})

    def test_bool_to_text(self):
        d = {
            "t": True,
            "f": False
        }
        self.assertEqual(splunk_dot_notation(d), {"t": "true", "f": "false"})

    @unittest.skipIf(PY3, "Long datatype doesn't exist in Python 3")
    def test_long(self):
        l = long(10000000000000000000000000000)
        self.assertEqual(splunk_dot_notation({"a": l}), {"a": l})

    def test_nested01(self):
        d = {
            "object": {"a": 1, "x": "two"},
            "array": ["1", "2", "3"]
        }
        e = {
            "object.a": 1,
            "object.x": "two",
            "array{}": ["1", "2", "3"]
        }
        output = splunk_dot_notation(d)
        self.assertEqual(output, e)

        d["array_of_objs"] = [
            {"a": 1, "z": 1},
            {"a": 2, "z": 2},
        ]
        e["array_of_objs{}.a"] = [1, 2]
        e["array_of_objs{}.z"] = [1, 2]
        output = splunk_dot_notation(d)
        self.assertEqual(output, e)

    def test_nested02(self):
        d = {
            "server": {
                "obj": [1, 2, 3]
            },
            "blah": {
                "a": 1,
                "b": 2,
                "c": [
                    {"a": 99},
                    {"a": 98}
                ],
            }
        }
        e = {
            "server.obj{}": [1, 2, 3],
            "blah.a": 1,
            "blah.b": 2,
            "blah.c{}.a": [99, 98],
        }
        output = splunk_dot_notation(d)
        self.assertDictEqual(output, e)
