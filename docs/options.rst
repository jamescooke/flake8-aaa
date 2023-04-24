Options and configuration
=========================

Flake8 can be invoked with ``--`` options *and* can read values from project
configuration files.

All names of Flake8-AAA's options and configuration values are prefixed with
"aaa". E.g. ``--aaa-act-block-style``.

Act block style
---------------

Command line flag
    ``--aaa-act-block-style``

Configuration option
    ``aaa_act_block_style``

The Act block style option adjusts how Flake8-AAA builds the Act block from the
Act node.

The allowed value is "default".

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
