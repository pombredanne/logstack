try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


description = """
logstack augments your stacktraces and logging by adding context.

Python has the ability to display stacktraces when required (through the
traceback module) or when exceptions occur. However, these only allow you to
see the current path down the code that the execution took; what the
application is doing, what it is doing it on, is always unclear.

Sure, you might want to fire up a debugger or log everything so that the
context is in there somewhere. But this is very heavy.

This modules allows you to log context, like you would with logging.info(), and
have this contextual information only pop up if an error occur. Furthermore,
this information can be inlined into your stacktrace, augmenting the raw line
numbers/method names with parameter values and custom messages.
"""
setup(name='logstack',
      version='0.1',
      packages=['logstack'],
      description='Augments your stacktraces and logging by adding context',
      author="Remi Rampin",
      author_email='remirampin@gmail.com',
      url='http://github.com/remram44/logstack',
      long_description=description,
      license='Apache License 2.0',
      keywords=['log', 'logging'],
      classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: Apache Software License",
        'Programming Language :: Python'])
