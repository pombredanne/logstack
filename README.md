stacklog: Augments your stacktraces and logging by adding context

# Introduction

Python has the ability to display stacktraces when required (through the traceback module) or when exceptions occur. However, these only allow you to see the current path down the *code* that the execution took; what the application is doing, what it is doing it on, is always unclear.

Sure, you might want to fire up a debugger or log everything so that the context is in there somewhere. But this is very heavy.

This modules allows you to log context, like you would with logging.info(), and have this contextual information only pop up if an error occur. Furthermore, this information can be inlined into your stacktrace, augmenting the raw line numbers/method names with parameter values and custom messages.

```
TODO : example stacktrace here
```

# Getting started

TODO
