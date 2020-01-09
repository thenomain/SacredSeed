import math

def header(self, text, width=None, *args, **kwargs):
    """
    Args:
        text: text, if any, to show
        self: command calling the header (optional)
        width: ...

    Returns:
        a pretty header

    This is harder than it seems, because Python's center() doesn't allow for multi-character strings,
    so we get to build our own.
    """
    caller = self.caller
    width = width or self.client_width()

    fillchar = "|c-|r=|n"

    width_text = len(text)

    divider = fillchar * (width - len(fillchar.clean()))
    len_left = math.floor((width - width_text)/2)
    len_right = math.ceil((width - width_text)/2)

    if text:
        return (divider / len_left) + " " + text + " " + (divider / len_right)
    else:
        return fillchar * 10


def footer(self, text):
    caller = self.caller
    if caller:
        return f"==== {text} ===="
    else:
        return f"---- {text} ----"
