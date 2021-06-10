""" Helper functions for custom Splunk Search Commands
"""


def ensure_fields(results):
    """ Ensure that the first result has a placeholder key for *ALL* the fields """
    # type: ignore (List[dict]) - > List[dict]
    # XXX: Make this smarter by only holding a fix number of results before moving on.
    # E.g. Assume no new fields after n rows with no new fields encountered
    field_set = set()
    output = []
    for result in results:
        field_set.update(result.keys())
        output.append(result)
    if output:
        # Apply *all* fields to the first result; all other rows are left alone
        # Q: Does this screw up field order?  (Not sure it's preserved in any case)
        output[0] = {k: output[0].get(k, None) for k in field_set}
    return output
