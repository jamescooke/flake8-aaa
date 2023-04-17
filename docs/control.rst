Controlling Flake8-AAA
======================

Options and configuration
-------------------------

Flake8 can be invoked with ``--`` options _and_ can read values from project
configuration files.

All names of Flake8-AAA's options and configuration values are prefixed with
"aaa". E.g. ``--aaa-act-block-style``.

Act block style
...............

Command line flag
    ``--aaa-act-block-style``

Configuration option
    ``aaa_act_block_style``

The Act block style option adjusts how Flake8-AAA builds the Act block from the
Act node.

The allowed value is "default".

Default mode

In default mode the Act block is the single Act node, best demonstrated by
example:

.. code-block:: python

    result = do_thing()

.. code-block:: python

    with pytest.raises(ValueError):
        do_thing()

The important feature of default Act blocks is that they do not contain any
context managers other than pytest or unittest ones.

.. code-block:: python

    def test_with():
        a_class = AClass()
        with freeze_time("2021-02-02 12:00:02"): 

            result = a_class.action('test')

        assert result == 'test'

In the example above, Flake8-AAA considers the ``with freeze_time()`` context
manager to be in the Arrange block. It therefore expects a blank line between
it and the ``result =`` Act block.

In code
-------

Flake8-AAA can be controlled using some special comments in your test code.

Explicitly marking blocks
.........................

One can set the act block explicitly using the ``# act`` comment. This is
necessary when there is no assignment possible.

See :ref:`AAA01: no Act block found in test - Correct code 2 <aaa01-correct-code-2>`.


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
