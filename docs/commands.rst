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

When Flake8-AAA finds the ``# noqa`` comment at the end of the line that
defines a test function, it will ignore it.

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

    $ python -m flake8_aaa ../some_test.py
    ------+------------------------------------------------------------------------
     1 DEF|def test():
     2 ARR|    x = 1
     3 ARR|    y = 1
     4 ACT|    result = x + y
               ^ AAA03 expected 1 blank line before Act block, found none
     5 BL |
     6 ASS|    assert result == 2
    ------+------------------------------------------------------------------------
        1 | ERROR
    $ echo "$?"
    1

And once the error above is fixed, the return value returns to zero::

    $ python -m flake8_aaa ../some_test.py
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
    $ echo "$?"
    0 

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

DEF
    Test function definition.

???
    Unprocessed line. Flake8-AAA has not categorised this line.
