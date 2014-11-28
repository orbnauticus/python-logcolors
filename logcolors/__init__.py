#!/usr/bin/env python

"""
Colorize logging messages

To activate, configure logging to use an instance of ColorStreamHandler. For
convenience, the output of handlers() can be passed to basicConfig:

>>> import logcolors

>>> logging.basicConfig(handlers=logcolors.handlers())

Color choices are available as instances of Color class, and can be passed as
keyword arguments to ColorStreamHandler

>>> logging.basicConfig(handlers=logcolors.handlers(
...    ERROR=Magenta))

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

Default colors are:

DEBUG: Blue
INFO: Cyan
WARNING: Yellow
ERROR: Red
CRITICAL: White.with_background(Red).with_bold()


"""


import logging
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL


class Color(object):
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

    def wrap(self, text):
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


class ColorStreamHandler(logging.StreamHandler):
    def __init__(self, **color_map):
        self.color_map = dict(
            DEBUG=Blue,
            INFO=Cyan,
            WARNING=Yellow,
            ERROR=Red,
            CRITICAL=White.with_background(Red).with_bold(),
        )
        self.color_map.update(color_map)
        super(ColorStreamHandler, self).__init__()

    @property
    def is_tty(self):
        try:
            return self.stream.isatty()
        except AttributeError:
            return False

    def emit(self, record):
        try:
            message = self.format(record)
            self.stream.write(message)
            self.stream.write(getattr(self, 'terminator', '\n'))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def format(self, record):
        message = logging.StreamHandler.format(self, record)
        if self.is_tty:
            message = self.color_map.get(record.levelname, Clear).wrap(message)
        return message


def handlers(**color_map):
    handler = ColorStreamHandler(**color_map)
    return [handler]
