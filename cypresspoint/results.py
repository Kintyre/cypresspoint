""" cypresspoint.results:  Tools for working with search results
"""

import gzip
import re
import sys
from collections import OrderedDict

if sys.version_info > (3,):
    from backports import csv
else:
    import csv

csv.field_size_limit(10485760)


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
