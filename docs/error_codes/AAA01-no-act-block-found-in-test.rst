AAA01: no Act block found in test
---------------------------------

An Act block is usually a line like ``result =`` or a check that an exception
is raised. Flake8-AAA could not find an Act block in the indicated test
function.

.. _aaa01-resolution:

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
None``, then ``mypy`` will complain if you try to assign a result. In this
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

.. note::

    Only Pytest context managers imported within the ``pytest`` namespace will
    be recognised when searching for Act blocks.

    E.g Flake8-AAA can find this context manager in the pytest namespace:

    .. code-block:: python

        import pytest

        def test() -> None:
            with pytest.raises(TypeError0:
                True[0]

    But this context manager will *not* be discovered:

    .. code-block:: python

        def test_imported() -> None:
            one_stuff = [1]

            with raises(IndexError):
                one_stuff[1]
