Good Examples
=============

All tests in all files in this directory conform to the current definition of
Arrange Act Assert as checked for by Flake8-AAA.

See `test_example.py <test_example.py>`_ for the simplest example of an
AAA-style test.

Valid tests
-----------

The goal is that all tests in both good and bad examples will target features
of the Python 3 standard library. They will all be executable with a vanilla
install of ``pytest``. Currently only the ``with`` statement examples support
this.

Testing Flake8-AAA
------------------

To prevent false negatives our test suite runs Flake8-AAA against this
directory and checks no linting errors are raised.
