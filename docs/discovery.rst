Test discovery
==============

The ``flake8-aaa`` plugin is triggered for files that look to it like test
modules - anything that does not look like a test module is skipped.

The following rules are applied by ``flake8-aaa`` when discovering tests:

* The module's filename must start with "test\_" and have been collected for
  linting by Flake8.

* Every function in the module that has a name that starts with "test" is
  checked.

* Test functions can be class methods.

* Test functions that contain only comments, docstrings or ``pass`` are
  skipped.

These rules are aimed to mirror pytest's default collection strategy as closely
as possible.

If you find that ``flake8-aaa`` is giving false positives (you have checks that
you expected to fail, but they did not), then you should check that the plugin
did not ignore or skip those tests which you expected to fail.

.. note::

    ``flake8-aaa`` does not check doctests.
