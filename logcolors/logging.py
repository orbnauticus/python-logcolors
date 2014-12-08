
"""

Colorize logging messages

To activate, configure logging to use an instance of ColorStreamHandler. For
convenience, the output of handlers() can be passed to basicConfig:

>>> from logging import basicConfig

>>> basicConfig(handlers=handlers())

Color choices are available as instances of Color class, and can be passed as
keyword arguments to ColorStreamHandler

>>> basicConfig(handlers=handlers(ERROR=Magenta))

Default colors are:

DEBUG: Blue
INFO: Cyan
WARNING: Yellow
ERROR: Red
CRITICAL: White.with_background(Red).with_bold()

"""
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL, StreamHandler

from .color import (Color, Clear, Black, Red, Green, Yellow, Blue, Magenta,
                    Cyan, White)


class ColorStreamHandler(StreamHandler):
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
        message = StreamHandler.format(self, record)
        if self.is_tty:
            message = self.color_map.get(record.levelname, Clear)(message)
        return message


def handlers(**color_map):
    handler = ColorStreamHandler(**color_map)
    return [handler]
