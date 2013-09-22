.. _reference:

Reference
=========

logstack is a very simple modules made up of different components: the
formatter, which allows the context stack to be printed from the :mod:`logging`
module, the stack-manipulating methods: :func:`~logstack.push` and
:func:`~logstack.pushed`, and the context class, set through
:func:`~logstack.set_context_class`.

Contexts
--------

Contexts are the objects that are pushed onto the logging stack. When you call
:func:`logstack.push`, the arguments are simply passed to the context class to
build an instance that is stored on the stack. That class thus determines the
signature of context-pushing methods; its :meth:`~object.__str__` method
determines how the contexts are rendered.

.. autofunction:: logstack.set_context_class

.. autoclass:: logstack.DefaultContext

Manipulating the stack
----------------------

In order for this module to have any effect, you need to add context
information. This information is associated with the stack, which means that
the context you add will be discarded when the current function returns. This
is so that when logging happens, only the relevant information gets printed
alongside the original message. You don't want to see what went right, you just
want to know what was going on when something wrong happens.

.. autofunction:: logstack.push

.. autofunction:: logstack.pushed
