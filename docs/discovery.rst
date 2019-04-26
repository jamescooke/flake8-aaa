Test discovery
==============

The Flake8-AAA plugin is triggered for files that look to it like test
modules - anything that does not look like a test module is skipped.

The following rules are applied by Flake8-AAA when discovering tests:

* The module's filename must start with "test\_" and have been collected for
  linting by Flake8.

* Every function in the module that has a name that starts with "test" is
  checked.

* Test functions can be class methods.

* Test functions that contain only comments, docstrings or ``pass`` are
  skipped.

These rules are aimed to mirror pytest's default collection strategy as closely
as possible.

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

Find Act node
.............

Search the test for the Act node which will indicate the existence of an Act
block. There are four recognised types of Act node:

``marked_act``
    Action is marked with Marked with ``# act`` comment::

        do_thing()  # act

``pytest_raises``
    Action is wrapped in ``pytest.raises`` context manager::

        with pytest.raises(ValueError):
            do_thing()

``result_assignment``
    Simple ``result =`` action::

        result = do_thing()

``unittest_raises``
    Action is wrapped in unittest's ``assertRaises`` context manager::

        with self.assertRaises(ValueError):
            do_thing()

Build Act block
...............

The Act node is used to build the Act block for the test. The Act block
contains all parent nodes of the Act node up to the test function. For
example::

    def test():
        with mock.patch('thing.thinger') as mock_thinger:   # < Act block first line
            with mock.patch('other_thing.thinger'):
                with pytest.raises(ValueError):             # < Act node
                    do_thing()                              # < Act block last line

        assert mock_thinger.call_count == 0

Build Arrange and Assert blocks
...............................

The Arrange block is created with all nodes in the test function that have a
line number before the start of the Act block.

The Assert block is created with all nodes in the test function that have a
line number after the end of the Act block.

Line-wise analysis
..................

Each block updates a list of line markers for the test and line-wise analysis
occurs to ensure that there is one and only one blank line between each block.
