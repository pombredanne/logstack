logstack: Augments your stacktraces and logging by adding context

[![Build Status](https://travis-ci.org/remram44/logstack.png?branch=master)](https://travis-ci.org/remram44/logstack)

# Introduction

Python has the ability to display stacktraces when required (through the [traceback] module) or when exceptions occur. However, these only allow you to see the current path down the *code* that the execution took; what the application is doing, what it is doing it on, is always unclear.

Sure, you might want to fire up a [debugger][pdb] or log everything so that the context is in there somewhere. But this is very heavy.

This modules allows you to log context, like you would with [logging.info()][logging.info], and have this contextual information only pop up if an error occur. Furthermore, this information can be inlined into your stacktrace, augmenting the raw line numbers/method names with parameter values and custom messages.

```
Traceback (most recent call last):
  File "getting_started.py", line 19, in <module>
    foo()
  File "getting_started.py", line 17, in foo
  starting up (in_foo=True)
    baz()
  File "getting_started.py", line 13, in baz
  (in_baz=True)
    raise ValueError("ohno")
ValueError: ohno
```

[traceback]: http://docs.python.org/library/traceback.html
[pdb]: http://docs.python.org/library/pdb.html
[logging.info]: http://docs.python.org/library/logging.html#logging.info

# Getting started

```python
import logging, logstack

# Setup: you need to do this somewhere before using logging or logstack
#
# Setup logging to log to the console (cf logging documentation)
console = logging.StreamHandler()
logging.getLogger().addHandler(console)
#
# Use the Formatter from logstack, it will add context to stack traces
console.setFormatter(logstack.Formatter())
#

# Example, generates the traceback above
def bar():
    # Adds context; bar() is not on the stack when logging, so won't be shown
    logstack.push("doing stuff", in_bar=True)
def baz():
    logstack.push(in_baz=True) # relevant context
    with logstack.pushed(something=[1, 2, 3]): # context for debug(),
        logging.debug("in block")              # discarded by logging level
                                               # along with the regular message
    raise ValueError("ohno")
def foo():
    logstack.push("starting up", in_foo=True)  # relevant context
    bar()
    baz()
try:
    foo()
except:
    logging.critical("Got an exception!", exc_info=True)
```
