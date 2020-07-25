Controlling Flake8-AAA
======================

In code
-------

Flake8-AAA can be controlled using some special comments in your test code.

Explicitly marking blocks
.........................

One can set the act block explicitly using the ``# act`` comment. This is
necessary when there is no assignment possible.

Disabling Flake8-AAA selectively
................................

When invoked via Flake8, Flake8 will filter any errors raised when lines are
marked with the ``# noqa`` syntax. You can turn off all errors from Flake8-AAA
by marking a line with ``# noqa: AAA`` and other Flake8 errors will still be
returned.

If you just want to ignore a particular error, then you can use the more
specific code and indicate the exact error to be ignored. For example, to
ignore the check for a space before the Act block, we can mark the Act block
with ``# noqa: AAA03``::

    def test():
        x = 1
        result = x + 1  # noqa: AAA03

        assert result == 2


.. _command-line:

Command line
------------

Flake8-AAA has a simple command line interface to assist with development and
debugging. Its goal is to show the state of analysed test functions, which
lines are considered to be parts of which blocks and any errors that have been
found.

Invocation, output and return value
...................................

With Flake8-AAA installed, it can be called as a Python module::

    $ python -m flake8_aaa [test_file]

Where ``[test_file]`` is the path to a file to be checked.

The return value of the execution is the number of errors found in the file,
for example::

    $ python -m flake8_aaa test_example.py
    ------+------------------------------------------------------------------------
     1 DEF|def test():
     2 ARR|    x = 1
     3 ARR|    y = 1
           ^ AAA03 expected 1 blank line before Act block, found none
     4 ACT|    result = x + y
     5 BL |
     6 ASS|    assert result == 2
    ------+------------------------------------------------------------------------
        1 | ERROR
    ======+========================================================================
            FAILED with 1 ERROR
    $ echo "$?"
    1

And once the error above is fixed, the return value returns to zero::

    $ python -m flake8_aaa test_example.py
    ------+------------------------------------------------------------------------
     1 DEF|def test():
     2 ARR|    x = 1
     3 ARR|    y = 1
     4 BL |
     5 ACT|    result = x + y
     6 BL |
     7 ASS|    assert result == 2
    ------+------------------------------------------------------------------------
        0 | ERRORS
    ======+========================================================================
            PASSED!
    $ echo "$?"
    0 

Only one file can be passed to the command line at a time. So to test all files
in a test suite, ``find`` should be used:

.. code-block:: shell

    $ find tests -name '*.py' | xargs -n 1 python -m flake8_aaa


noqa and command line
.....................

The ``# noqa`` comment marker works slightly differently when Flake8-AAA is
called on the command line rather than invoked through ``flake8``. When called
on the command line, to skip linting a test function, mark the function
definition with ``# noqa`` on the same line as the ``def``.

For example::

    def test_to_be_ignored(  # noqa
        arg_1,
        arg_2,
    ):
        ...

.. _line-markers:

Line markers
............

Each test found in the passed file is displayed. Each line is annotated with
its line number in the file and a marker to show how Flake8-AAA classified that
line. Line markers are as follows:

ACT
    Line is part of the Act Block.

ARR
    Line is part of an Arrange Block.

ASS
    Line is part of the Assert Block.

BL
    Line is considered a blank line for layout purposes.

CMT
    Line is a ``#`` comment.

DEF
    Test function definition.

???
    Unprocessed line. Flake8-AAA has not categorised this line.
