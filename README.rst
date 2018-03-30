.. image:: https://img.shields.io/travis/jamescooke/flake8-aaa/master.svg
    :target: https://travis-ci.org/jamescooke/flake8-aaa/branches
    :alt: Travis build


flake8-aaa plugin
=================

A `flake8 <http://flake8.pycqa.org/en/latest/index.html>`_ plugin for linting
Python tests against the rules of the `Arrange Act Assert pattern
<http://jamescooke.info/arrange-act-assert-pattern-for-python-developers.html>`_
of testing.

Error codes
-----------

AAA01: No result variable set in test
.....................................

Act blocks are expected to assign the test result to a ``result``
variable. If you can't set a ``result``, then mark the line considered
the Act block with ``# aaa act`` (case insensitive).

AAA02: Multiple results assigned
................................

There should only be one result assigned per test. If you have a test that
contains more than one ``result =`` statement, then consider splitting that
test into multiple tests.
