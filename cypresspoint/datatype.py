"""

"""

from __future__ import unicode_literals

import re
from datetime import timedelta


def reltime_to_timedelta(value):
    pattern = re.compile(r"(\d+)([dhms]?)")
    suffix_map = {
        "s": "seconds",
        "m": "minutes",
        "h": "hours",
        "d": "days",
    }
    m = pattern.match(value)
    if m is None:
        raise ValueError("Unsupported span value: '{0}'  "
                         "Supports formats like '7d', '2h', and '15m'".format(value))
    v, suffix = m.groups()
    try:
        v = int(v)
    except ValueError:
        raise ValueError("Unsupported value: '{0}'".format(value))
    if not suffix:
        suffix = "s"
    td_arg = suffix_map[suffix]
    kwargs = {td_arg: v}
    return timedelta(**kwargs)


def as_bool(s):
    return s.lower()[0] in ("t", "y", "e", "1")
