""" cypresspoint.results:  Tools for working with search results
"""


import re


def expand_vars(string, context, log=None):
    """ Expand vars in strings.   $var$
    Very quick-n-dirty!
    """
    def rep(match_obj):
        var = match_obj.group(1)
        if var == "":
            # Replace "$$" with a literal "$"
            return "$"
        else:
            return context.get(var)

    result = re.sub(r'\$([\w._]*)\$', rep, string)
    if result != string:
        if log is callable:
            log("Expanded '{}' to '{}'".format(string, result))
    return result
