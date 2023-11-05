Test discovery and analysis
===========================

Flake8-AAA filters the Python code passed to it by Flake8. It finds lines that
looks like test code and then checks those lines match the AAA pattern. When
all checks pass no error is raised.

File filtering
--------------

First, the filename is checked. It must match one of the following patterns:

* Is called ``test.py`` or ``tests.py``.

* Starts with ``test_``, i.e match ``test_*.py``

* Ends with ``_test.py``, i.e. match ``*_test.py``.

For every file that matches the patterns above, Flake8-AAA checks every
function and class method whose name starts with "test".

Test functions and methods that contain only comments, docstrings or ``pass``
are skipped.

Rationale
.........

The aim of this process is to mirror `Pytest's default collection strategy
<https://docs.pytest.org/en/7.2.x/explanation/goodpractices.html#test-discovery>`_
as closely as possible. It also aims to work with popular testing tutorials
such as Django's `Writing your first Django app
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
therefore not counted:

.. code-block:: python

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
    Action is marked with Marked with ``# act`` comment:

    .. code-block:: python

        do_thing()  # act

``pytest_raises``
    Action is wrapped in one of Pytest's context managers: ``pytest.raises()``,
    ``pytest.warns()`` or ``pytest.deprecated_call()``:

    .. code-block:: python

        with pytest.raises(ValueError):
            do_thing()

``result_assignment``
    ``result =`` action:

    .. code-block:: python

        result = do_thing()

``unittest_raises``
    Action is wrapped in unittest's ``assertRaises`` context manager:

    .. code-block:: python

        with self.assertRaises(ValueError):
            do_thing()

Flake8-AAA searches each test function for lines that look like Act blocks. It
will raise an error when a function does not have exactly 1 Act block.

However, note assertions that exceptions are raised can also be used in Assert
blocks. When Flake8-AAA finds a suitable ``marked_act`` or
``result_assignment`` node, it will allow ``pytest_raises`` nodes in the Assert
block.

The "act block style" configuration allows for a "large" style of Act block to
be specified, which changes how Act blocks are built in relation to context
managers. See :ref:`Act block style option <option-act-block-style>`.

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
