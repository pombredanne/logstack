import contextlib
import linecache
import logging
import sys
import threading
import traceback
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from .purging_map import PurgingMap


# Gets the current frame (from logging)
def currentframe():
    try:
        raise Exception
    except:
        return sys.exc_info()[2].tb_frame.f_back
if hasattr(sys, '_getframe'): currentframe = lambda: sys._getframe(1)


class StackMap(PurgingMap):
    def set(self, key, value):
        frames = set()
        f = key
        while f is not None:
            frames.add(f)
            f = f.f_back
        self.filter(frames)
        super(StackMap, self).set(key, value)


class DefaultContext(object):
    """Default context formatter.
    """
    def __init__(self, msg=None, **kwargs):
        self.msg = msg
        self.kwargs = kwargs

    def __str__(self):
        if self.kwargs:
            kw = ', '.join('%s=%r' % (k, v)
                           for k, v in self.kwargs.iteritems())
            if self.msg:
                return "%s (%s)" % (self.msg, kw)
            else:
                return "(%s)" % kw
        elif self.msg:
            return self.msg


_context_class = DefaultContext


def set_context_class(cls):
    """Changes the class used to build/format contexts.

    This class gets passed the arguments that were given to push() or pushed(),
    and is converted to a string to be put in the traceback.
    """
    global _context_class
    _context_class = cls


localstorage = threading.local()

def infos():
    if not hasattr(localstorage, 'pushed_infos'):
        localstorage.pushed_infos = StackMap()
    return localstorage.pushed_infos


class ExceptionFormatterMixin(object):
    """Logging formatter that inserts the context objects in the traceback.
    """
    def formatException(self, ei):
        etype, value, tb = ei[:3]
        formatted = []
        formatted.append("Traceback (most recent call last):")
        while tb is not None:
            f = tb.tb_frame
            lineno = tb.tb_lineno
            co = f.f_code
            filename = co.co_filename
            name = co.co_name
            item = '  File "%s", line %d, in %s' % (filename, lineno, name)

            frame_contexts = infos().get(f)
            if frame_contexts:
                for ctx in frame_contexts:
                    item += '\n  %s' % ctx

            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            if line:
                item += '\n    ' + line.strip()

            formatted.append(item)
            tb = tb.tb_next
        formatted.append("%s: %s" % (etype.__name__, value.message))
        return '\n'.join(formatted)


class Formatter(ExceptionFormatterMixin, logging.Formatter):
    """Version of logging.Formatter with the custom traceback.
    """


def push(*args, **kwargs):
    """Push some context onto the stack.

    You don't have to pop this, it is associated with the caller's stack frame.
    """
    f = currentframe().f_back
    infos().set(f, _context_class(*args, **kwargs))


@contextlib.contextmanager
def pushed(*args, **kwargs):
    """Push some context onto the stack.

    The context is removed when leaving the context manager.
    """
    ctx = _context_class(*args, **kwargs)
    f = currentframe().f_back
    i = infos()
    i.set(f, ctx)
    try:
        yield
    finally:
        i.remove(f, ctx)
