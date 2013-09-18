from __future__ import with_statement

import logstack
import logging


logger = logging.getLogger()


format = logstack.Formatter("%(asctime)s %(levelname)s:\n%(message)s")
console = logging.StreamHandler()
console.setFormatter(format)
logger.addHandler(console)


def bar():
    logstack.push(in_bar=True)

def baz():
    logstack.push(in_baz=True)
    with logstack.pushed(something=[1, 2, 3]):
        logger.warning("warning here")
    raise ValueError("ohno")

def foo():
    logstack.push(in_foo=True)
    bar()
    logstack.push(out_of_bar=True)
    baz()

try:
    foo()
except:
    logger.critical("Got an exception!", exc_info=True)
