AAA01: no Act block found in test
---------------------------------

An Act block is usually a line like ``result =`` or a check that an exception
is raised. When Flake8-AAA raises ``AAA01`` it could not find an Act block in
the indicated test function.

Problematic code
................

.. code-block:: python

    def test_some_text():
        some = 'some'
        text = 'text'

        some_text = f'{some}_{text}'

        assert some_text == 'some_text'

Correct code 1
..............

Use ``result =``.

.. code-block:: python

    def test_some_text():
        some = 'some'
        text = 'text'

        result = f'{some}_{some}'

        assert result == 'some_text'

Correct code 2
..............

Mark your Act block with the ``# act`` hint.

.. code-block:: python

    def test_some_text():
        some = 'some'
        text = 'text'

        some_text = f'{some}_{text}'  # act

        assert some_text == 'some_text'

Rationale
.........

Exceptions
..........


Resolution
..........

Add an Act block to the test or mark a line that should be considered the
action.

Even if the result of a test action is ``None``, assign that result and
pin it with a test:

.. code-block:: python

    result = action()

    assert result is None

However, if your action's ``None`` return value is type-hinted ``action() ->
None``, then ``mypy`` might complain if you try to assign a result. In this
case, or any other where a you can not assign a ``result``, then mark the end
of the line considered the Act block with ``# act`` (case insensitive):

.. code-block:: python

    data['new_key'] = 1  # act

If the action spans multiple lines, then it can be marked with ``# act`` on the
first or last line. Both of the following will work:

.. code-block:: python

    validate_row(  # act
        {"total_number_of_users": "1", "number_of_new_users": "0"},
        ["total_number_of_users", "number_of_new_users"],
    )

    validate_row(
        {"total_number_of_users": "1", "number_of_new_users": "0"},
        ["total_number_of_users", "number_of_new_users"],
    )  # act

Code blocks wrapped in ``pytest.raises()`` and ``unittest.assertRaises()``
context managers are recognised as Act blocks.
