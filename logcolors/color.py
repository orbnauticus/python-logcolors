
"""

Black, Red, Green, Yellow, Blue, Magenta, Cyan, White

Clear can be used for the default text color

>>> Clear == Color(None, None, False)
True

Add a background color using with_background method:

>>> White.with_background(Red)
Color(7, 1, False)

Turn bold on and off using with_bold. Default is True:

>>> White.with_bold()
Color(7, None, True)

>>> White.with_bold(False)
Color(7, None, False)
"""


class Color(object):
    """
    >>> print(Red('Red Text'), 'Clear',
    ...       White.with_background(Black)("White on Black"))
    \x1b[31mRed Text\x1b[0m Clear \x1b[37;40mWhite on Black\x1b[0m
    """
    def __init__(self, foreground, background=None, bold=False):
        self.foreground = foreground
        self.background = background
        self.bold = bold

    def with_background(self, background_color):
        return self.__class__(
            self.foreground,
            background_color.foreground,
            self.bold,
        )

    def with_bold(self, bold=True):
        return self.__class__(
            self.foreground,
            self.background,
            bold,
        )

    def __call__(self, text):
        return '\x1b[{codes}m{text}\x1b[0m'.format(
            codes=';'.join(code for code in (
                None if self.foreground is None else str(self.foreground + 30),
                None if self.background is None else str(self.background + 40),
                '1' if self.bold else '',
            ) if code),
            text=text,
        )

    def __repr__(self):
        return 'Color({}, {}, {})'.format(
            self.foreground,
            self.background,
            self.bold,
        )

    def __eq__(self, other):
        return ((self.foreground == other.foreground) and
                (self.background == other.background) and
                (self.bold == other.bold))


Clear = Color(None)
Black = Color(0)
Red = Color(1)
Green = Color(2)
Yellow = Color(3)
Blue = Color(4)
Magenta = Color(5)
Cyan = Color(6)
White = Color(7)
