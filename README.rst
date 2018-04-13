.. image:: https://img.shields.io/travis/jamescooke/flake8-aaa/master.svg
    :target: https://travis-ci.org/jamescooke/flake8-aaa/branches
    :alt: Travis build


flake8-aaa plugin
=================

A `flake8 <http://flake8.pycqa.org/en/latest/index.html>`_ plugin for linting
Python tests against the rules of the `Arrange Act Assert pattern
<http://jamescooke.info/arrange-act-assert-pattern-for-python-developers.html>`_
of testing.

Resources
---------

* `Changelog <CHANGELOG.rst>`_


Docs
====

(to be extracted to RTD)


Test discovery
--------------

* Filename must start with ``test_`` and have been collected for linting by
  ``flake8``.

* Test must be a function where its name starts with ``test``.

* Tests that contain only comments, docstrings or ``pass`` are skipped.


Error codes
-----------

AAA01: no Act block found in test
:::::::::::::::::::::::::::::::::

Test found to have no Act block.

An Act block is usually a line like ``result =`` or a check that an exception
is raised using ``with pytest.raises(Exception):``.

Resolution
..........

Add an Act block to the test or mark a line that should be considered the
action.

Even if the result of a test action is ``None``, assign that result and test
it::

    result = action()

    assert result is None

If you can't set a ``result``, then mark the end of the line considered the Act
block with ``# act`` (case insensitive)::

    data['new_key'] = 1  # act

AAA02: multiple Act blocks found in test
::::::::::::::::::::::::::::::::::::::::

There must be one and only one Act block in every test. The linter found more
than one potential Act block in this test.

A test that contains more than one ``result =`` statement or more than one line
marked ``# act`` creates ambiguity and raises this error code.

Resolution
..........

Splitting the failing test into multiple tests. Where there is complicated or
reused set-up code then that should be extracted into fixtures.
