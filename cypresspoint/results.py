""" cypresspoint.results:  Tools for working with search results
"""

import gzip
import re
import sys

if sys.version_info < (3,):
    # For consistent unicode support
    from backports import csv
else:
    import csv

csv.field_size_limit(10485760)


_expand_styles = {
    "$": (re.compile(r'\$([\w._]*)\$'), "$"),
    "{}": (re.compile(r'\{([\w._-]*)\}'), "{}"),
}


def expand_vars(string, context, style="$", log=None):
    """ Expand vars in strings.   $var$
    Very quick-n-dirty!

    Note that expanding '$var$' format only works in result fields not in
    paramaters.  That is because Splunk already does $var$ expansion on it's on,
    and anything that doesn't match is replaced with an empty string.  You can
    of course use $result.fieldname$, but this only works on the first result
    row and then you don't need this function.

    Given this limitation, support for '{field}' variable expansion was added.
    Maybe someday additional field formatting options could be supported too,
    like what Python supports natively, but for now only simple varable
    substitution works.
    """
    regex, literal = _expand_styles[style]

    def rep(match_obj):
        var = match_obj.group(1)
        if var == "":
            # Replace "$$" with "$", or "{}"" with "{}"
            return literal
        else:
            return context.get(var)

    result = regex.sub(rep, string)
    if result != string:
        if log is callable:
            log("Expanded '{}' to '{}'".format(string, result))
    return result


def _decode_mv_field(field,
                     mv_field_re=re.compile(r'\$((?:\$\$|[^$])*)\$(?:;|$)')):
    return [m.replace("$$", "$") for m in mv_field_re.findall(field)]


def get_job_results(results_file, encoding="utf8"):
    """
    Read in results from a results file (results.csv.gz)
    Generate: dict
    """
    if not results_file.endswith(".csv.gz"):
        raise NotImplementedError("Expecting results file to be a .csv.gz file.")

    mv_fields = None
    with gzip.open(results_file, "rt", encoding=encoding) as stream:
        for row in csv.DictReader(stream):
            # Remove __mv_ fields; replacing the origion fields with lists of values, were necessary
            if mv_fields is None:
                mv_fields = [(f, f[5:]) for f in row if f.startswith("__mv_")]
            if mv_fields:
                for mv_field, field in mv_fields:
                    if row[mv_field]:
                        row[field] = _decode_mv_field(row[mv_field])
                    del row[mv_field]
            yield row
