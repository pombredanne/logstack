logstack: Augments your stacktraces and logging by adding context

[![Build Status](https://travis-ci.org/remram44/logstack.png?branch=master)](https://travis-ci.org/remram44/logstack)

# Introduction

Python has the ability to display stacktraces when required (through the [traceback] module) or when exceptions occur. However, these only allow you to see the current path down the *code* that the execution took; what the application is doing, what it is doing it on, is always unclear.

Sure, you might want to fire up a [debugger][pdb] or log everything so that the context is in there somewhere. But this is very heavy.

This modules allows you to log context, like you would with [logging.info()][logging.info], and have this contextual information only pop up if an error occur. Furthermore, this information can be inlined into your stacktrace, augmenting the raw line numbers/method names with parameter values and custom messages.

```
TODO : example stacktrace here
```

[traceback]: http://docs.python.org/library/traceback.html
[pdb]: http://docs.python.org/library/pdb.html
[logging.info]: http://docs.python.org/library/logging.html#logging.info

# Getting started

TODO
