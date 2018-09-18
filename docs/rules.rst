Rules and error codes
=====================

The rules applied by ``flake8-aaa`` are from the `Arrange Act Assert pattern
for Python developers
<https://jamescooke.info/arrange-act-assert-pattern-for-python-developers.html>`_.

.. note::

    The rules applied by ``flake8-aaa`` are only a subset of the rules and
    guidelines of the Arrange Act Assert pattern itself. Please see `the
    published guidelines for the pattern
    <https://jamescooke.info/arrange-act-assert-pattern-for-python-developers.html>`_
    and read these rules in the context of the definition there.

AAA01: no Act block found in test
---------------------------------

An Act block is usually a line like ``result =`` or a check that an exception
is raised. ``flake8-aaa`` could not find an Act block in the indicated test
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

There must be one and only one Act block in every test but ``flake8-aaa`` found
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
Arrange and Act blocks, but ``flake8-aaa`` could not find one.

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
and Assert blocks, but ``flake8-aaa`` could not find one.

This blank line creates separation between the action and the assertions and
makes the Act block easy to spot.

As with rule ``AAA03``, this rule works best with ``E303`` enabled.

Resolution
..........

Add a blank line before the Assert block.
