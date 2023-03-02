"""
A collection of Python 2/3 compatibility functions.

This is kept for backwards compatibility, but this should eventually be
depreciated and removed.
"""

from datetime import datetime


def dt_to_epoch(ts: datetime) -> int:
    """ Convert datetime to an Unix epoch value

    :param datetime ts: timestamp
    :rtype: int
    """
    # TODO:  Do some kind of python deprecated warning here
    return int(ts.timestamp())
