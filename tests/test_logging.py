from __future__ import with_statement

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
        self.assertEqual(
                self.output.getvalue(),
'WARNING\n'
'warning here\n'

'CRITICAL\n'
'Got exception\n'
'Traceback (most recent call last):\n'
'  File "C:\\programmation\\logstack\\tests\\test_logging.py", line 38, in '
        'test_logging\n'
'    foo()\n'
'  File "C:\\programmation\\logstack\\tests\\test_logging.py", line 25, in '
        'foo\n'
'  (in_foo=True)\n'
'  (out_of_bar=True)\n'
'    baz()\n'
'  File "C:\\programmation\\logstack\\tests\\test_logging.py", line 20, in '
        'baz\n'
'  (in_baz=True)\n'
'    raise ValueError("ohno")\n'
'ValueError: ohno\n')
