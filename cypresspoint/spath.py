import re
from typing import Any, List, Tuple


def sanitize_fieldname(field: str) -> str:
    """ Remove unwanted characters from the provided field name.  The goal is to
    mimic the general field cleanup behavior of Splunk """
    clean = re.sub(r'[^A-Za-z0-9_.{}\[\]-]', "_", field)
    # Remove leading/trailing underscores
    clean = clean.strip("_")
    return clean


def _dict_to_splunk_fields(obj: Any, prefix: Tuple[str] = ()
                           ) -> List[Tuple[Tuple[str, str], str]]:
    """
    Input:  Object   (dict, list, str/int/float)
    Output:  [  ( (name,name), value) ]

    Convention:  Arrays suffixed with "{}"
    """
    output = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            key = sanitize_fieldname(key)
            output.extend(_dict_to_splunk_fields(value, prefix=prefix+(key,)))
    elif isinstance(obj, (list)):
        if prefix:
            prefix = prefix[:-1] + (prefix[-1] + "{}",)
            for item in obj:
                output.extend(_dict_to_splunk_fields(item, prefix=prefix))
    elif isinstance(obj, bool):
        output.append((prefix, "true" if obj else "false"))
    elif isinstance(obj, (str, int, float)) or obj is None:
        output.append((prefix, obj))
    else:
        raise TypeError("Unsupported datatype {}".format(type(obj)))
    return output


def splunk_dot_notation(obj: dict) -> dict:
    """
    Convert json object (python dictionary) into a list of fields as Splunk does by default.
    Think of this as the same as calling Splunk's "spath" SPL command.
    """
    d = {}
    if not isinstance(obj, dict):
        raise ValueError("Expected obj to be a dictionary, received {}"
                         .format(type(obj)))
    for field_pair, value in _dict_to_splunk_fields(obj):
        field_name = ".".join(field_pair)
        if field_name in d:
            if not isinstance(d[field_name], list):
                d[field_name] = [d[field_name]]
            d[field_name].append(value)
        else:
            d[field_name] = value
    return d
