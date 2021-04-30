""" Hot in-place fixes for splunklib (Splunk's Python SDK)

NOTE: Simply importing this module will activate the monkeypatch.
"""

from __future__ import unicode_literals


def _monkey_patch_splunk_xml_parser():
    """ Return APP to know which app contains the inputs.conf stanza

    <stanza name="mod_input://MyInput" app="search">

    Hopefully this becomes unnecessary in the future:
    https://github.com/splunk/splunk-sdk-python/pull/371
    """
    # We store the 'app' in '__app' for later access.  This was chosen because
    # '__' is never used by apps, and it fits with other workarounds already
    # present in the splunk-sdk.

    import splunklib.modularinput.utils

    def parse_xml_data(parent_node, child_node_tag):
        from splunklib.modularinput.utils import parse_parameters
        data = {}
        for child in parent_node:
            if child.tag == child_node_tag:
                if child_node_tag == "stanza":
                    data[child.get("name")] = {}
                    # Added line here:
                    data[child.get("name")]["__app"] = child.get("app", None)
                    for param in child:
                        data[child.get("name")][param.get("name")] = parse_parameters(param)
            elif "item" == parent_node.tag:
                data[child.get("name")] = parse_parameters(child)
        return data

    splunklib.modularinput.utils.parse_xml_data = parse_xml_data

    import splunklib.modularinput.input_definition
    splunklib.modularinput.input_definition.parse_xml_data = parse_xml_data


_monkey_patch_splunk_xml_parser()
