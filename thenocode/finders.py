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
    here = caller.location

    if "," in targets_string:
        delimiter = ","
    else:
        delimiter = " "

    targets_list = [t.strip() for t in targets_string.split(delimiter)]
    targets = []

    for t in targets_list:
        found = caller.search(t)
        if (found is not None) and (found not in targets):  # for each target that is not already in targets...
            if not include_disconnected:
                if (not found.is_connected) and (not found == here):
                    caller.msg(f"'{found}' is not connected.")
                else:
                    targets.append(found)
            # shouldn't there be an 'else: targets.append(found)' here?

    if (here not in targets) and (caller not in targets):
        targets += [caller]

    if (here in targets) and (len(targets) > 1):
        targets = [target for target in targets if target not in here.contents]

    return targets
