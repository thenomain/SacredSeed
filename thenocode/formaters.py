import math
import evennia.utils.ansi as ansi
"""
There is a lot of repetition here because the exact way these borders look will change drastically from game to game.
"""


def header(self, text, width=None):
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
    border = style_border_repeats("|h|x=|h|b=|n", width)

    if text:
        text = ansi.ANSIString(f"|n|h< {text} >|n")
        border = insert_text_centered(border, text)

    return border


def footer(self, text, width=None):
    width = width or self.client_width() or 80
    border = style_border_repeats("|h|b=|h|x=|n", width)

    if text:
        text = ansi.ANSIString(f"|n|h< {text} >|n")
        border = insert_text_right_just(border, text, 4)

    return border


def divider(self, text, width=None):
    width = width or self.client_width() or 80
    border = style_border_repeats("|h|x-|h|b-|n", width)

    if text:
        text = ansi.ANSIString(f"|x|h|| |n{text} |x|h|||n")
        border = insert_text_centered(border, text)

    return border

# -----------------
# support functions
# -----------------


def style_border_repeats(pattern, width):
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


def style_border_mirrored(pattern, width):
    """
    e.g.,
        -=-=-=#> <#=-=-=-
    Args:
        pattern: pattern to output, then mirror
        width: width

    Returns:
        border_left: the pattern repeated
        border_right: border_left reversed
    """
    pass


def insert_text_centered(border, text):
    """
    Take a completed border and jam the text centered in the middle of it.
    This preserves the border's
    Args:
        border: the horizontal border to insert text into
        text: the text to insert

    Returns:

    """
    text_width = len(text)
    width = len(border)

    # centered
    len_left = math.floor((width - text_width) / 2)
    len_right = len_left + text_width

    border_left = border[0:len_left]
    border_right = border[len_right:width]

    return border_left + text + border_right


def insert_text_right_just(border, text, offset=0):
    """
    e.g.,
        ----------------------< text >--
    Args:
        border:
        text:
        offset:

    Returns:

    """
    text_width = len(text)
    width = len(border)

    len_left = width - text_width - offset
    len_right = -offset

    border_left = border[0:len_left]
    border_right = border[len_right:width]

    return border_left + text + border_right


def insert_text_left_just(border, text, offset=0):
    """
    e.g.,
        --< text >----------------------
    Args:
        border:
        text:
        offset:

    Returns:

    """
    text_width = len(text)
    width = len(border)

    len_left = -offset
    len_right = width - text_width - offset

    border_left = border[0:len_left]
    border_right = border[len_right:width]

    return border_left + text + border_right
