import linecache
import logging
import os
import sys
import threading
import traceback

from .purging_map import PurgingMap, SynchronizedPurgingMap


def enable_parachute(crashlog):
    global StackMap

    def _tracing_func(frame, event, *args):
        if event == 'return':
            frames = set()
            f = frame.f_back
            while f is not None:
                frames.add(f)
                f = f.f_back
            infos().filter(frames)

    class StackMap(SynchronizedPurgingMap):
        threadnum = 0
        threadnum_mutex = threading.Lock()

        def __init__(self):
            with self.threadnum_mutex:
                num = StackMap.threadnum
                StackMap.threadnum += 1
            SynchronizedPurgingMap.__init__(
                    self,
                    os.path.join(crashlog, 'thread_%d.log' % num))

        def set(self, key, value):
            if sys.getprofile() != _tracing_func:
                sys.setprofile(_tracing_func)
            super(StackMap, self).set(key, value)

    sys.setprofile(_tracing_func)


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

    It takes an optional message and any number of parameters, passed as
    keyword arguments.

    For example, using::

        logstack.push("Opening a file", filename="foo.txt", mode="r")

    will display::

        Opening a file (filename="foo.txt", mode="r")
    """
    def __init__(self, msg=None, **kwargs):
        self.msg = msg
        self.kwargs = kwargs

    def __str__(self):
        if self.kwargs:
            kw = ', '.join('%s=%r' % (k, v)
                           for k, v in self.kwargs.items())
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

    The default is :class:`~DefaultContext` which takes a message and keyword
    parameters.
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
    def format(self, record):
        self.__record = record
        return super(ExceptionFormatterMixin, self).format(record)

    def formatException(self, ei):
        try:
            fmt = self.__record.logstack
        except AttributeError:
            fmt = None # default is 'full'
        if fmt == 'stack':
            stack = True
            contexts = False
        elif fmt == 'contexts':
            stack = False
            contexts = True
        else:
            stack = True
            contexts = True

        etype, value, tb = ei[:3]
        formatted = []
        formatted.append("Traceback (most recent call last):\n")
        while tb is not None:
            f = tb.tb_frame
            lineno = tb.tb_lineno
            co = f.f_code
            filename = co.co_filename
            name = co.co_name
            item = ''
            if stack:
                item += '  File "%s", line %d, in %s\n' % (
                        filename, lineno, name)

            if contexts:
                frame_contexts = infos().get(f)
                if frame_contexts:
                    for ctx in frame_contexts:
                        item += '  %s\n' % ctx

            if stack:
                linecache.checkcache(filename)
                line = linecache.getline(filename, lineno, f.f_globals)
                if line:
                    item += '    %s\n' % line.strip()

            formatted.append(item)
            tb = tb.tb_next
        formatted.append("%s: %s" % (etype.__name__, value))
        return ''.join(formatted)


class Formatter(ExceptionFormatterMixin, logging.Formatter):
    """Version of logging.Formatter with the custom traceback.
    """
    def __init__(self, *args, **kwargs):
        logging.Formatter.__init__(self, *args, **kwargs)


def push(*args, **kwargs):
    """Push some context onto the stack.

    You don't have to pop this, it is associated with the caller's stack frame.
    """
    f = currentframe().f_back
    infos().set(f, _context_class(*args, **kwargs))


class pushed(object):
    """Push some context onto the stack.

    The context is removed when leaving the context manager.
    """
    def __init__(self, *args, **kwargs):
        self.ctx = _context_class(*args, **kwargs)

    def __enter__(self):
        self.frame = currentframe().f_back
        infos().set(self.frame, self.ctx)

    def __exit__(self, exc_type, exc_val, exc_tb):
        infos().remove(self.frame, self.ctx)
