AAA05: blank line in block
==========================

The only blank lines in the test must be around the Act block making it easy to
spot. Flake8-AAA found additional blank lines which break up the block's
layout.

Problematic code
----------------

.. code-block:: python

    def test_a() -> None:
        x = 3

        y = 4

        result = x**2 + y**2

        assert result == 25

.. code-block:: python

    def test_b() -> None:
        nothing = None

        with pytest.raises(AttributeError):

            nothing.get_something()

Correct code
------------

Remove the blank lines.

.. code-block:: python

    def test_a() -> None:
        x = 3
        y = 4

        result = x**2 + y**2

        assert result == 25

.. code-block:: python

    def test_b() -> None:
        nothing = None

        with pytest.raises(AttributeError):
            nothing.get_something()

Rationale
---------

Blank lines are essential for dividing up a test. There will usually be just
two blank lines in each test - one above and one below the Act block. They
serve to separate the Act block from the rest of the test.

When there are additional blank lines in a test, then the "shape" of the test
is broken and it is hard to see where the Act block is at a glance.
