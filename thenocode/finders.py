def build_targets_list(self, targets_string):
    """
    Function to build a target list on the following criteria:
        "here" returns the location object of the enactor
        otherwise looks for corresponding character objects

    Args:
        self: class object of Command or MuxCommand type
        targets_string: space- or comma-delimited list of names

    Returns:
        list[] of objects found, 'here' returning caller's containing room

    """
    caller = self.caller

    if "," in targets_string:
        delimiter = ","
    else:
        delimiter = " "

    targets = [target.strip() for target in targets_string.split(delimiter)]  # remove spaces around each element
    targets = [caller.search(target) for target in set(targets)]  # search each element, report misfires, remove repeats
    targets = [target for target in targets if target]  # remove empty elements

    if (caller.location not in targets) and (caller not in targets):
        targets += [caller]

    if (caller.location in targets) and (len(targets) > 1):
        targets = [target for target in targets if target not in caller.location.contents]

    return targets
