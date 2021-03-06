r"""
Evennia settings file.

The available options are found in the default settings file found
here:

/Users/fubar/Documents/Projects/Evennia/evennia/evennia/settings_default.py

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "SacredSeed"

######################################################################
# Default command sets and commands
######################################################################

# Insert an inheritance layer below MuxCommand, for styles
# (This does not require updating Objects in the database.)
# step 1: below
# step 2: In commands.command, add:
#         from evennia.commands.default.muxcommand import MuxCommand as BaseMuxCommand

COMMAND_DEFAULT_CLASS = "commands.command.MuxCommand"

######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
