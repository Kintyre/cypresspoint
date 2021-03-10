def _monkey_patch_splunk_xml_parser():
    """ Need to return "APP", so we know which app contains that stanzas where we update the inputs.conf file.

    <stanza name="mod_input://MyInput" app="search">
    """

    import splunklib.modularinput.utils

    def parse_xml_data(parent_node, child_node_tag):
        from splunklib.modularinput.utils import parse_parameters
        data = {}
        for child in parent_node:
            if child.tag == child_node_tag:
                if child_node_tag == "stanza":
                    data[child.get("name")] = {}
                    # My change.  Because '__' is never used by apps, and that's the kind of wonky crap the splunk-sdk does ;-(
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
