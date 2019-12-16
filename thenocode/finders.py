def build_targets_list(self, targets_string, include_disconnected=True):
    """
    Function to build a target list on the following criteria:
        "here" returns the location object of the enactor
        otherwise looks for corresponding character objects

    Args:
        self: class object of Command or MuxCommand type
        targets_string: space- or comma-delimited list of names
        include_disconnected: should disconnected characters on list be kept? (default: True)

    Returns:
        list[] of objects found, 'here' returning caller's containing room
    """

    caller = self.caller

    if "," in targets_string:
        delimiter = ","
    else:
        delimiter = " "

    targets = [t.strip() for t in targets_string.split(delimiter)]  # remove spaces around each element
    targets = [caller.search(t) for t in set(targets)]  # search each element, report misfires, remove repeats
    targets = [t for t in targets if t]  # remove empty elements

    if not include_disconnected:
        for i, t in enumerate(targets):
            if (not t.is_connected) or (not t == caller.location):
                caller.msg(f"{t} is not connected")
                targets.remove(i)
        # targets = [t for t in targets if (not t.is_connected) or (not t == caller.location)]

    if (caller.location not in targets) and (caller not in targets):
        targets += [caller]

    if (caller.location in targets) and (len(targets) > 1):
        targets = [target for target in targets if target not in caller.location.contents]

    return targets
