"""

"""

import re
from datetime import timedelta


def reltime_to_timedelta(value: str) -> timedelta:
    """Convert a relative time expression into a Python timedelta object.
    Only a subset of Splunk's relative time syntax is supported, but many simple
    expressions like ``7d`` (7 days), ``5m`` (5 mins), ``6mon`` (6 months),
    and ``2y`` (2 years) should just work.

    This does *not* support snapping with ``@``.
    At this time relative times addition (``+``) or subtraction (``-``)
    is not yet supported, but should be.

    :param value: Relative time expression
    :type value: str
    :return: python object representation of the given relative time
    :rtype: timedelta
    """
    pattern = re.compile(r"(\d+)(mon|[dhmswy]?)")
    suffix_map = {
        "s": "seconds",
        "m": "minutes",
        "h": "hours",
        "d": "days",
        "w": "weeks",
    }
    suffix_day_multiplier = {
        "y": 365,
        "mon": 30,
    }
    m = pattern.match(value)
    if m is None:
        raise ValueError("Unsupported span value: '{0}'  "
                         "Supports formats like '3y', '6mon', '3w', '7d', "
                         "'2h' and '15m'".format(value))
    v, suffix = m.groups()
    try:
        v = int(v)
    except ValueError:
        raise ValueError("Unsupported value: '{0}'".format(value))
    if not suffix:
        suffix = "s"
    td_arg = suffix_map.get(suffix, "days")
    multiplier = suffix_day_multiplier.get(suffix, 1)
    kwargs = {td_arg: v * multiplier}
    return timedelta(**kwargs)


def as_bool(s):
    """Convert a boolean-like configuration field into a proper boolean.

    :param s: Input string containing some form of truthy value
    :type s: str
    :rtype: bool
    """
    if s is None or isinstance(s, bool):
        return s
    try:
        return s.lower()[0] in ("t", "y", "e", "1")
    except AttributeError as e:
        raise ValueError(e)
