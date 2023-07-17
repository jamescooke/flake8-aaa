Command line
============

Flake8-AAA **had** a simple command line interface to assist with development
and debugging.

Line markers are documented below, but may be removed later.

.. _line-markers:

Line markers
------------

The following markers / types indicate how Flake8-AAA classifies the lines of
code is parses relative to its role in the test.

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
