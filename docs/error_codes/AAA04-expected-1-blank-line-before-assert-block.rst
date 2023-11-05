AAA04: expected 1 blank line before Assert block, found none
============================================================

For tests that have an Assert block, there must be a blank line between the Act
and Assert blocks, but Flake8-AAA could not find one.

Prerequisites
-------------

This rule works best with `pycodestyle
<https://pypi.org/project/pycodestyle/>`_'s ``E303`` rule enabled because it
ensures that there are not multiple blank lines between the blocks.

Problematic code
----------------

.. code-block:: python

    def test() -> None:
        x = 3

        result = x**5
        assert result == 243

Correct code
------------

Add a blank line before the Assert block.

.. code-block:: python

    def test() -> None:
        x = 3

        result = x**5

        assert result == 243

Rationale
---------

This blank line creates separation between the action and the assertions - it
makes the Act block easy to spot.
