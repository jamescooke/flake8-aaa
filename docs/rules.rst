Rules and error codes
=====================

The rules applied by Flake8-AAA are from the `Arrange Act Assert pattern
for Python developers
<https://jamescooke.info/arrange-act-assert-pattern-for-python-developers.html>`_.

.. note::

    The rules applied by Flake8-AAA are only a subset of the rules and
    guidelines of the Arrange Act Assert pattern itself. Please see `the
    published guidelines for the pattern
    <https://jamescooke.info/arrange-act-assert-pattern-for-python-developers.html>`_
    and read these rules in the context of the definition there.

.. note::

    Flake8-AAA works best with the following Flake8 rules enabled:

    * ``E303`` "too many blank lines"
    * ``E702`` "Multiple statements on one line"


AAA01: no Act block found in test
---------------------------------

An Act block is usually a line like ``result =`` or a check that an exception
is raised. Flake8-AAA could not find an Act block in the indicated test
function.

Resolution
..........

Add an Act block to the test or mark a line that should be considered the
action.

Even if the result of a test action is ``None``, assign that result and
pin it with a test::

    result = action()

    assert result is None

If you can not assign a ``result``, then mark the end of the line considered
the Act block with ``# act`` (case insensitive)::

    data['new_key'] = 1  # act

Code blocks wrapped in ``pytest.raises()`` and ``unittest.assertRaises()``
context managers are recognised as Act blocks.

AAA02: multiple Act blocks found in test
----------------------------------------

There must be one and only one Act block in every test but Flake8-AAA found
more than one potential Act block. This error is usually triggered when a test
contains more than one ``result =`` statement or more than one line marked ``#
act``. Multiple Act blocks create ambiguity and raise this error code.

Resolution
..........

Split the failing test into multiple tests. Where there is complicated or
reused set-up code then apply the DRY principle and extract the reused code
into one or more fixtures.

AAA03: expected 1 blank line before Act block, found none
---------------------------------------------------------

For tests that have an Arrange block, there must be a blank line between the
Arrange and Act blocks, but Flake8-AAA could not find one.

This blank line creates separation between the arrangement and the action and
makes the Act block easy to spot.

This rule works best with `pycodestyle
<https://pypi.org/project/pycodestyle/>`_'s ``E303`` rule enabled because it
ensures that there are not multiple blank lines between the blocks.

Resolution
..........

Add a blank line before the Act block.

AAA04: expected 1 blank line before Assert block, found none
------------------------------------------------------------

For tests that have an Assert block, there must be a blank line between the Act
and Assert blocks, but Flake8-AAA could not find one.

This blank line creates separation between the action and the assertions and
makes the Act block easy to spot.

As with rule ``AAA03``, this rule works best with ``E303`` enabled.

Resolution
..........

Add a blank line before the Assert block.

AAA05: blank line in block
--------------------------

The only blank lines in the test must be around the Act block making it easy to
spot. Flake8-AAA found additional blank lines which break up the block's
layout.

Resolution
..........

Remove the blank line.

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

AAA99: collision when marking this line as NEW_CODE, was already OLD_CODE
-------------------------------------------------------------------------

This is an error code that is raised when Flake8 tries to mark a single line as
occupied by two different types of block. It *should* never happen. The values
for ``NEW_CODE`` and ``OLD_CODE`` are from the list of :ref:`line-markers`.

Resolution
..........

Please open a `new issue
<https://github.com/jamescooke/flake8-aaa/issues/new>`_ containing the output
for the failing test as generated by the :ref:`command-line` tool.

You could hack around with your test to see if you can get it to work while
waiting for someone to reply to your issue. If you're able to adjust the test
to get it to work, that updated test would also be helpful for debugging.
