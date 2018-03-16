flake8-aaa plugin
=================

A `flake8 <http://flake8.pycqa.org/en/latest/index.html>`_ plugin for linting
Python tests against the rules of the `Arrange Act Assert pattern
<http://jamescooke.info/arrange-act-assert-pattern-for-python-developers.html>`_
of testing.

Error codes
-----------

======= =====================
Code    Message and rule info
======= =====================
AAA01   No result variable set in test.

        Act blocks are expected to assign the test result to a `result`
        variable. If you can't set a `result`, then mark the line considered
        the test action with `#noqa AAA01`.
======= =====================
