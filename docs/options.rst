Options and configuration
=========================

Flake8 can be invoked with ``--`` options *and* can read values from project
configuration files.

All names of Flake8-AAA's options and configuration values are prefixed with
"aaa". E.g. ``--aaa-act-block-style``.

.. _option-act-block-style:

Act block style
---------------

Command line flag
    ``--aaa-act-block-style``

Configuration option
    ``aaa_act_block_style``

The Act block style option adjusts how Flake8-AAA builds the Act block from the
Act node.

The allowed values are "default" and "large".

Default
.......

In default mode the Act block is the single Act node, best demonstrated by
example:

.. code-block:: python

    result = do_thing()

Or...

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

.. _large-act-block-style:

Large
.....

Large style Act blocks have been provided to be compatible with Black.

In Large mode the Act block can grow to include context managers that wrap it.
For example, referring to the test above, this would be formatted as follows
with Large Act blocks:

.. code-block:: python

    def test_with():
        a_class = AClass()

        with freeze_time("2021-02-02 12:00:02"): 
            result = a_class.action('test')

        assert result == 'test'

The ``result =`` result assignment Act block expands to include the
``freeze_time()`` context manager. In this way, the blank line that divides the
Arrange block from the Act block can be *before* the context manager - a format
which is compatible with Black.

Note however, the context manager only joined the Act block because the Act
node was the **first** line in the context manager's body. If we moved the
``AClass()`` initialisation inside the context manager, something different
would happen:

.. code-block:: python

    def test_with():
        with freeze_time("2021-02-02 12:00:02"): 
            a_class = AClass()

            result = a_class.action('test')

        assert result == 'test'

This time the result assignment does *not* consume the context manager.
Instead, the ``freeze_time()`` context manager and the ``a_class``
initialisation make up the Arrange block, and there's a single blank line
between that and the simple result assignment Act block.
