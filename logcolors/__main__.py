
import logging
import logcolors

logging.basicConfig(
    level=logging.DEBUG,
    handlers=logcolors.handlers(),
)

logging.getLogger('blue').debug('THIS IS A DEBUG MESSAGE')
logging.getLogger('cyan').info('THIS IS AN INFO MESSAGE')
logging.getLogger('yellow').warning('THIS IS A WARNING MESSAGE')
logging.getLogger('red').error('THIS IS AN ERROR MESSAGE')
logging.getLogger('white on red bold').critical('THIS IS A CRITICAL MESSAGE')
