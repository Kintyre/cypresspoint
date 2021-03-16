"""
A collection of Python 2/3 compatibility functions.

These should go away when Splunk 7.3 support is dropped.
"""


def dt_to_epoch(ts):
    """ Convert datetime to an Unix epoch value

    :param datetime ts: timestamp
    :rtype: int
    """
    try:
        # Python 3
        return int(ts.timestamp())
    except AttributeError:
        # XXX:  This isn't always as accurate if timezones are involved....
        return int(ts.strftime("%s"))
