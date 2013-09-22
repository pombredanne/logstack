.. _index:

logstack: a context stack to complement your logging
====================================================

Getting started
---------------

This simple example will show you how to setup :mod:`logging` and logstack and
log some simple messages to the console, with context::

   import logging, logstack

   console = logging.StreamHandler()
   console.setFormatter(logstack.Formatter())
   logging.getLogger().addHandler(console)

   def bar():
       logstack.push("doing stuff", in_bar=True) # irrelevant context
   def baz():
       logstack.push(in_baz=True) # relevant context
       with logstack.pushed(something=[1, 2, 3]): # context for debug(),
           logging.debug("in block")              # discarded with it
       raise ValueError("ohno")
   def foo():
       logstack.push("starting up", in_foo=True) # relevant context
       bar()
       baz()
   try:
       foo()
   except:
       logging.critical("Got an exception!", exc_info=True) # triggers logging

In this example, the following trace will be printed::

   Got an exception!
   Traceback (most recent call last):
     File "getting_started.py", line 23, in <module>
       foo()
     File "getting_started.py", line 20, in foo
     starting up (in_foo=True)
       baz()
     File "getting_started.py", line 15, in baz
     (in_baz=True)
       raise ValueError("ohno")
   ValueError: ohno

Here, the ``doing stuff (in_bar=True)`` message was not displayed because the
function finished without logging anything. This makes the logfile much clearer
because contextual information stays contextual, i.e. is only shown to shed
light on an actual event.

Note that, except when pushing contexts, the standard :mod:`logging` module is
used; though a special Formatter with the custom traceback logic must be used.

Contents
--------

.. toctree::
   :maxdepth: 2

   reference
   internals
   changelog

Links
-----

* `The excellent standard logging module <docs.python.org/library/logging.html>`_
* `The structlog library, similar in some ways <https://github.com/hynek/structlog>`_

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
