AAA06: comment in Act block
---------------------------

Problematic code
................

.. code-block:: python

    def test() -> None:
        shopping = ['apples', 'bananas', 'cabbages']

        # Reverse shopping list operates in place
        shopping.reverse()  # act

        assert shopping == ['cabbages', 'bananas', 'apples']

Correct code
............

.. code-block:: python

    def test() -> None:
        """
        Reverse shopping list operates in place
        """
        shopping = ['apples', 'bananas', 'cabbages']

        shopping.reverse()  # act

        assert shopping == ['cabbages', 'bananas', 'apples']

Rationale
.........

The Act block carries out a single action on an object. It is the focus of each
test. Therefore any comments on this single action are really comments on the
test itself and so should be moved to the test docstring.

By placing these important comments in the docstring we can:

* Make it easier to keep the Act block simple.

* Help to distinguish the Act block from the rest of the test.

* Improve the documentation of tests because any important comments and notes
  are lifted to the top of the test.

Exceptions
..........

Inline comments used to pass information to linters are OK:

* Marking the Act block:

  .. code-block:: python

      shopping.reverse()  # act

* Marking lines in the action for linting reasons:

  .. code-block:: python

      result = shopping.reverse()  # type: ignore