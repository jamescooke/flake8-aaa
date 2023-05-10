AAA06: comment in Act block
===========================

Problematic code
----------------

.. code-block:: python

    def test_a() -> None:
        shopping = ['apples', 'bananas', 'cabbages']

        # Reverse shopping list operates in place
        shopping.reverse()  # act

        assert shopping == ['cabbages', 'bananas', 'apples']

.. code-block:: python

    def test_b() -> None:
        # NOTE: the most interesting thing about this test is this comment
        result = 1 + 1

        assert result == 2

Correct code
------------

Use docstrings instead of hash-comments:

.. code-block:: python

    def test_a() -> None:
        """
        Reverse shopping list operates in place
        """
        shopping = ['apples', 'bananas', 'cabbages']

        shopping.reverse()  # act

        assert shopping == ['cabbages', 'bananas', 'apples']

.. code-block:: python

    def test_b() -> None:
        """
        NOTE: the most interesting thing about this test is this comment
        """
        result = 1 + 1

        assert result == 2

Separate hash-comment line from Act block with a blank line:

.. code-block:: python

    def test_b() -> None:
        # NOTE: the most interesting thing about this test is this comment

        result = 1 + 1

        assert result == 2

Rationale
---------

The Act block carries out a single action on an object. It is the focus of each
test. Therefore any comments on this single action are really comments on the
test itself and so should be moved to the test docstring.

By placing these important comments in the docstring we can:

* Make it easier to keep the Act block simple.

* Help to distinguish the Act block from the rest of the test.

* Improve the documentation of tests because any important comments and notes
  are lifted to the top of the test.

Exceptions
----------

Directives in the form of inline comments are OK, for example:

* Marking the Act block:

  .. code-block:: python

      shopping.reverse()  # act

* Marking lines in the action for linting reasons:

  .. code-block:: python

      result = shopping.reverse()  # type: ignore
