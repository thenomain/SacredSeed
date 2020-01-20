import math
import evennia.utils.ansi as ansi


def header(self, text, width=None, *args, **kwargs):
    """
    Args:
        text: text, if any, to show
        self: command calling the header (optional)
        width: A certain width passed, or None

    Returns:
        a pretty header

    This is harder than it seems, because Python's center() doesn't allow for multi-character strings,
    so we get to build our own.
    """
    width = width or self.client_width() or 80

    divider_pattern = ansi.ANSIString("|c-|r=|n")
    width_fill = len(divider_pattern)
    divider = divider_pattern * (width - width_fill)

    if text:
        text = ansi.ANSIString(f"|n|h {text} |n")
        width_text = len(text)
        len_left = math.floor((width - width_text) / 2)
        len_right = width - len_left

        divider_left = divider[0:len_left]
        divider_right = divider[len_right:width]

        return divider_left + text + divider_right
    else:
        return divider


def footer(self, text):
    caller = self.caller
    if caller:
        return f"==== {text} ===="
    else:
        return f"---- {text} ----"
