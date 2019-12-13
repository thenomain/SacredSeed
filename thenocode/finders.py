def build_search_list(self, targets_string):
    """
    Function to build a target list on the following criteria:
        "here" expands to all objects in self's location
        otherwise the string list of names looks for corresponding character objects

    Args:
        self: class object of Command or MuxCommand type
        targets_string: space- or comma-delimited list of names

    Returns:
        list[] of objects found

    """
    caller = self.caller
    here = caller.location

    if "," in targets_string:
        delimiter = ","
    else:
        delimiter = " "

    targets = [target.strip() for target in targets_string.split(delimiter)]  # remove spaces around each element
    targets = [caller.search(target) for target in set(targets)]  # search each element, reporting misfires
    targets = [target for target in targets if target]  # remove empty elements

    if here in targets:
        targets.remove(here)
        targets += here.contents

    targets = list(set().union(*[targets]))  # get rid of redundant targets

    return targets
