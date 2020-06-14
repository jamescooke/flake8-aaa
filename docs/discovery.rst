Test discovery and analysis
===========================

When running as a Flake8 plugin, Flake8-AAA filters the Python code passed to
it by Flake8. It finds code that looks like test code and then checks that code
matches the AAA pattern. When all checks pass, then no error is raised.

Filtering
---------

First, the filename is checked. It must either ``test.py``, ``tests.py`` or
start with ``test_``. For those files that match, every function that has a
name that starts with "test" is checked. This includes class methods.

Test functions and methods that contain only comments, docstrings or ``pass``
are skipped.

The aim of this process is to mirror Pytest's default collection strategy as
closely as possible. It also aims to work with popular testing tutorials such
as Django's `Writing your first Django app
<https://docs.djangoproject.com/en/3.0/intro/tutorial05/#create-a-test-to-expose-the-bug>`_
which states:

    Put the following in the ``tests.py`` file in the polls application

If you find that Flake8-AAA is giving false positives (you have checks that
you expected to fail, but they did not), then you should check that the plugin
did not ignore or skip those tests which you expected to fail.

.. note::

    Flake8-AAA does not check doctests.

Processing
----------

For each test found, Flake8-AAA runs the following processes, most of which can
be found in ``Function.check_all()``.

Check for no-op
...............

Skip test if it is considered "no-op" (``pass``, docstring, etc).

Mark blank lines
................

Mark all lines in the test that have no characters and are not part of a
string. For example, the following snipped contains only one blank line (line 3
- in the middle of the list), the second at line 9 is part of a string and
therefore not counted::

    assert result == [
        1,

        2,
    ]
    # Check on output
    assert str(result) == """[
    1,

    2,
    ]"""

Mark comments
.............

All lines that are ``#`` comment lines are marked.

.. code-block:: python

    # This line is considered a comment line

    result = item.act()  # But not this line

This process relies on analysing the tokens that make up the test.

Find the Act block
..................

There are four recognised types of Act block:

``marked_act``
    Action is marked with Marked with ``# act`` comment::

        do_thing()  # act

``pytest_raises``
    Action is wrapped in ``pytest.raises`` context manager::

        with pytest.raises(ValueError):
            do_thing()

``result_assignment``
    ``result =`` action::

        result = do_thing()

``unittest_raises``
    Action is wrapped in unittest's ``assertRaises`` context manager::

        with self.assertRaises(ValueError):
            do_thing()

Flake8-AAA searches each test function for lines that look like Act blocks. It
will raise an error when a function does not have exactly 1 Act block.

Build Arrange and Assert blocks
...............................

The Arrange block is created with all nodes in the test function that have a
line number before the start of the Act block.

The Assert block is created with all nodes in the test function that have a
line number after the end of the Act block.

Line-wise analysis
..................

Finally a line-by-line analysis of the test function is carried out to ensure
that:

* No blocks contain extra blank lines.

* There is a single blank line above and below the Act block.
