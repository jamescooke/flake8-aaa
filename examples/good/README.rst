Good Examples
=============

All tests in all files in this directory conform to the current definition of
Arrange Act Assert as checked for by Flake8-AAA.

See `test_example.py <test_example.py>`_ for the simplest example of an
AAA-style test.

Valid tests
-----------

All good and bad tests are intended to work on Python 3 stdlib. They are tested
with vanilla ``pytest`` to ensure they pass in the ``examples`` environment.

Testing Flake8-AAA
------------------

To prevent false negatives our test suite runs Flake8-AAA against all test
modules in this directory and checks no linting errors are raised.
