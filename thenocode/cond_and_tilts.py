# let's see if we can add conditions & tilts to django
#  cd SacredSeed/world
#  evennia startapp myapp

import json

persistence = {
    0: "No",
    1: "Yes",
    2: "Maybe"
}

# import the jsons and mush them together
json_conditions = ""
dumped_conditions = json.dumps(json_conditions, indent=4)  # Check what this is for, e.g. if needed.
