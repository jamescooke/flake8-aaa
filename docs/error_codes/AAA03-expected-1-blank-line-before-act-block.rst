AAA03: expected 1 blank line before Act block, found none
=========================================================

For tests that have an Arrange block, there must be a blank line between the
Arrange and Act blocks, but Flake8-AAA could not find one.

Prerequisites
-------------

This rule works best with `pycodestyle
<https://pypi.org/project/pycodestyle/>`_'s ``E303`` rule enabled because it
ensures that there are not multiple blank lines between the blocks.

If test code is formatted with Black, then it's best to set :ref:`"large" Act
block style <large-act-block-style>`.

Problematic code
----------------

.. code-block:: python

    def test_simple(hello_world_path: pathlib.Path) -> None:
        with open(hello_world_path) as f:
            result = f.read()

        assert result == 'Hello World!\n'

Correct code
------------

Since the ``open()`` context manager is part of the Arrange block, create space
between it and the ``result =`` Act block.

.. code-block:: python

    def test_simple(hello_world_path: pathlib.Path) -> None:
        with open(hello_world_path) as f:

            result = f.read()

        assert result == 'Hello World!\n'

Alternatively, if you want the context manager to be treated as part of the Act
block, the :ref:`"large" Act block style <large-act-block-style>` as mentioned
above.

Rationale
---------

This blank line creates separation between the test's Arrange and Act blocks
and makes the Act block easy to spot.
