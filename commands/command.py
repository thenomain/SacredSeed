"""
Commands

Commands describe the input the account can do to the game.

"""

# Insert an inheritance layer below MuxCommand, for styles
# (This does not require updating Objects in the database.)
# step 1: In server.conf.settings, add
#         COMMAND_DEFAULT_CLASS = "commands.command.MuxCommand"
# step 2: below

import math
from evennia.commands.default.muxcommand import MuxCommand as BaseMuxCommand
import evennia.utils.ansi as ansi

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
    def styled_header(self, text=None, width=None):
        """
        Args:
            self: command calling the header
            text: text, if any, to show
            width: A certain width passed, or None

        Returns:
            a pretty header

        This is harder than it seems, because Python's center() doesn't allow for multi-character strings,
        so we get to build our own.
        """
        width = width or self.client_width() or 80
        pattern = "|h|x=|h|b=|n"
        border = self.style_border_repeats(pattern, width)

        if text:
            text = ansi.ANSIString(f"|n|h< {text} >|n")
            border = self.insert_text_centered(border, text)

        return border

    def styled_footer(self, text=None, width=None):
        width = width or self.client_width() or 80
        pattern = "|h|b=|h|x=|n"
        border = self.style_border_repeats(pattern, width)

        if text:
            text = ansi.ANSIString(f"|n|h< {text} >|n")
            border = self.insert_text_right_just(border, text, 4)

        return border

    def styled_divider(self, text=None, width=None):
        width = width or self.client_width() or 80
        pattern = "|h|x-|h|b-|n"
        border = self.style_border_repeats(pattern, width)

        if text:
            text = ansi.ANSIString(f"|x|h|| |n{text} |x|h|||n")
            border = self.insert_text_centered(border, text)

        return border

    # -----------------
    # support functions
    # -----------------

    def style_border_repeats(self, pattern, width):
        """
        Take some text and return it exactly to width.
        e.g.,
            -=-=-=-=-=-=-=-=-=-=-=-=-=
        Args:
            pattern: the pattern that's going to be repeated
            width: width, usually of the client screen

        Returns:
            a border line that is exactly 'width' wide
        """

        style_pattern = ansi.ANSIString(pattern)
        style_width = len(style_pattern)
        # +1 to assure that substring always shortens.
        # See Issue #2030: https://github.com/evennia/evennia/issues/2030
        # Remove the +1 when issue is resolved.
        border = style_pattern * (math.ceil(width / style_width) + 1)

        # clip pattern to 'width'
        return border[0:width]

    def style_border_mirrors(self, pattern, width):
        """
        e.g.,
            -=>-=>-=> <=-<=-<=-
            -=<>-=<>-=<> <>=-<>=-<>=-

        Args:
            pattern: pattern to output, then mirror
            width: width

        Returns:
            border_left: the pattern repeated
            border_right: border_left reversed
        """
        pass

    def insert_text_centered(self, border, text):
        """
        Take a completed border and jam the text centered in the middle of it.
        This preserves the border's
        Args:
            border: the horizontal border to insert text into
            text: the text to insert

        Returns:
            new border

        """
        text_width = len(text)
        width = len(border)

        # centered
        len_left = math.floor((width - text_width) / 2)
        len_right = len_left + text_width

        border_left = border[0:len_left]
        border_right = border[len_right:width]

        return border_left + text + border_right

    def insert_text_right_just(self, border, text, offset=0):
        """
        e.g.,
            ----------------------< text >--
        Args:
            border: rendered border
            text: text to insert
            offset: how many characters to leave on the right

        Returns:
            new border

        """
        text_width = len(text)
        width = len(border)

        len_left = width - text_width - offset
        len_right = -offset

        border_left = border[0:len_left]
        border_right = border[len_right:width]

        return border_left + text + border_right

    def insert_text_left_just(self, border, text, offset=0):
        """
        e.g.,
            --< text >----------------------
        Args:
            border:
            text:
            offset: how many characters to leave on the left

        Returns:

        """
        text_width = len(text)
        width = len(border)

        len_left = -offset
        len_right = width - text_width - offset

        border_left = border[0:len_left]
        border_right = border[len_right:width]

        return border_left + text + border_right
