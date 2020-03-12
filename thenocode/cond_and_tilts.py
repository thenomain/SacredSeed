# conditions & tilts

import json

conditions_persistence = {
    0: "No",
    1: "Yes",
    2: "Maybe"
}

# import the jsons and mush them together
json_conditions = ""
json_tilts = ""
dumped_conditions = json.dumps(json_conditions, indent=4)  # Check what this is for, e.g. is it needed.
dumped_tilts = json.dumps(json_tilts, indent=4)  # Check what this is for, e.g. is it needed.
