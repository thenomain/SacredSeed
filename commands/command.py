"""
Commands

Commands describe the input the account can do to the game.

"""

# Insert an inheritance layer below MuxCommand, for styles
# (This does not require updating Objects in the database.)
# step 1: In server.conf.settings, add
#         COMMAND_DEFAULT_CLASS = "commands.command.MuxCommand"
# step 2: below

from evennia.commands.default.muxcommand import MuxCommand as BaseMuxCommand

# -------------------------------------------------------------
#
# The default commands inherit from
#
#   evennia.commands.default.muxcommand.MuxCommand.
#
# If you want to make sweeping changes to default commands you can
# uncomment this copy of the MuxCommand parent and add
#
#   COMMAND_DEFAULT_CLASS = "commands.command.MuxCommand"
#
# to your settings file. Be warned that the default commands expect
# the functionality implemented in the parse() method, so be
# careful with what you change.
#
# -------------------------------------------------------------


class MuxCommand(BaseMuxCommand):
    """
    Inherit from this if you want to create your own command styles
    from scratch.  Note that Evennia's default commands inherits from
    MuxCommand instead.

    Note that the class's `__doc__` string (this text) is
    used by Evennia to create the automatic help entry for
    the command, so make sure to document consistently here.

    Each Command implements the following methods, called
    in this order (only func() is actually required):
        - at_pre_cmd(): If this returns anything truthy, execution is aborted.
        - parse(): Should perform any extra parsing needed on self.args
            and store the result on self.
        - func(): Performs the actual work.
        - at_post_cmd(): Extra actions, often things done after
            every command, like prompts.

    """

    # override styles from evennia.commands.command
    def styled_header(self, message=None, *args, **kwargs):
        """
        Create a pretty header.
        """
        # return f"----- {message} -----"
        pass
        # if "mode" not in kwargs:
        #     kwargs["mode"] = "separator"
        # return self._render_decoration(*args, **kwargs)
