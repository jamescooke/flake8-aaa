AAA02: multiple Act blocks found in test
========================================

Flake8-AAA checks that every test has a single, clear Act block.

When Flake8-AAA raises ``AAA02`` it found more than one Act block in a
particular test.

Problematic code
----------------

.. code-block:: python

    def test() -> None:
        x = 1
        y = 2

        result = x + y

        assert result == 3
        result = 2 * x + 2 * y
        assert result == 6

Correct code
------------

Split the one test with two Act blocks into two distinct tests.

.. code-block:: python

    def test_A() -> None:
        x = 1
        y = 2

        result = x + y

        assert result == 3

    def test_B() -> None:
        x = 1
        y = 2

        result = 2 * x + 2 * y

        assert result == 6

Rationale
---------

Each test carries out a single action and tests its result.

Having multiple actions in a test create ambiguity because it can become less
clear which behaviour is being tested.

Where there is complicated or reused set-up code, then apply the DRY principle
and extract the reused code into one or more fixtures.
