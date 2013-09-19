from __future__ import with_statement

import itertools
import re
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import logging
import logstack


def bar():
    logstack.push(in_bar=True)
def baz():
    logstack.push(in_baz=True)
    with logstack.pushed(something=[1, 2, 3]):
        logging.warning("warning here")
    raise ValueError("ohno")
def foo():
    logstack.push(in_foo=True)
    bar()
    logstack.push(out_of_bar=True)
    baz()


class TestLogging(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger()
        self.output = StringIO.StringIO()
        console = logging.StreamHandler(self.output)
        console.setFormatter(logstack.Formatter("%(levelname)s\n%(message)s"))
        self.logger.addHandler(console)

    def test_logging(self):
        try:
            foo()
        except:
            logging.critical("Got exception", exc_info=True)
        expected = (
r'^WARNING$',
r'^warning here$',

r'^CRITICAL$',
r'^Got exception$',
r'^Traceback \(most recent call last\):$',
r'^  File ".+test_logging\.py", line [0-9]+, in test_logging$',
r'^    foo\(\)$',
r'^  File ".+test_logging\.py", line [0-9]+, in foo$',
r'^  \(in_foo=True\)$',
r'^  \(out_of_bar=True\)$',
r'^    baz\(\)$',
r'^  File ".+test_logging\.py", line [0-9]+, in baz$',
r'^  \(in_baz=True\)$',
r'^    raise ValueError\("ohno"\)$',
r'^ValueError: ohno$')
        actual = self.output.getvalue().split('\n')
        if actual and not actual[-1]:
            actual = actual[:-1]
        for a, e in itertools.izip_longest(actual, expected):
            self.assertIsNotNone(re.search(e, a), "%r != %r" % (a, e))
