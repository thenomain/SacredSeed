def build_search_list(self, targets_string):
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
    # here = caller.location

    if "," in targets_string:
        delimiter = ","
    else:
        delimiter = " "

    targets = [target.strip() for target in targets_string.split(delimiter)]  # remove spaces around each element
    targets = [caller.search(target) for target in set(targets)]  # search each element, reporting misfires
    targets = [target for target in targets if target]  # remove empty elements

    if (caller.location not in targets) and (caller not in targets):
        targets += [caller]

    if caller.location in targets:
        # targets_set = set(targets)
        # targets_set= set(targets).difference(set(caller.location.contents))
        # targets = list(targets_set)
        targets = list(set(targets).difference(set(caller.location.contents)))

    targets = list(set().union(*[targets]))  # get rid of redundant targets

    return targets
