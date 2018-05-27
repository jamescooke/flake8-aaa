Rules and error codes
=====================

AAA01: no Act block found in test
---------------------------------

Test found to have no Act block.

An Act block is usually a line like ``result =`` or a check that an exception
is raised using ``with pytest.raises(Exception):``.

Resolution
..........

Add an Act block to the test or mark a line that should be considered the
action.

Even if the result of a test action is ``None``, assign that result and pint it
with a test::

    result = action()

    assert result is None

If you can not assign a ``result``, then mark the end of the line considered
the Act block with ``# act`` (case insensitive)::

    data['new_key'] = 1  # act

AAA02: multiple Act blocks found in test
----------------------------------------

There must be one and only one Act block in every test. The linter found more
than one potential Act block in this test.

A test that contains more than one ``result =`` statement or more than one line
marked ``# act`` creates ambiguity and raises this error code.

Resolution
..........

Splitting the failing test into multiple tests. Where there is complicated or
reused set-up code then that should be extracted into one or more fixtures.
