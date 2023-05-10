AAA01: no Act block found in test
=================================

An Act block is usually a line like ``result =`` or a check that an exception
is raised. When Flake8-AAA raises ``AAA01`` it could not find an Act block in
the indicated test function.

Problematic code
----------------

.. code-block:: python

    def test_some_text() -> None:
        some = 'some'
        text = 'text'

        some_text = f'{some}_{text}'

        assert some_text == 'some_text'

.. code-block:: python

    from pytest import raises

    def test() -> None:
        with raises(IndexError):
            list()[0]

Correct code 1
--------------

Use ``result =`` assignment to indicate the action in the test:

.. code-block:: python

    def test_some_text() -> None:
        some = 'some'
        text = 'text'

        result = f'{some}_{some}'

        assert result == 'some_text'

Ensure all Pytest context managers are in the ``pytest`` namespace - use
``pytest.raises()`` not just ``raises()``:

.. code-block:: python

    import pytest

    def test() -> None:
        with pytest.raises(IndexError):
            list()[0]

.. _aaa01-correct-code-2:

Correct code 2
--------------

Alternatively, mark your Act block with the ``# act`` hint to indicate the
action in the test. This can be useful for scenarios where a result can not be
assigned, such as tests on functions that return ``None``.

.. code-block:: python

    def test_some_text() -> None:
        some = 'some'
        text = 'text'

        some_text = f'{some}_{text}'  # act

        assert some_text == 'some_text'

.. code-block:: python

    from pytest import raises

    def test() -> None:
        with raises(IndexError):
            list()[0]  # act

Rationale
---------

The Act block carries out a single action on an object so it's important that
Flake8-AAA can clearly distinguish which line or lines make up the Act block in
every test.

Flake8-AAA recognises code blocks wrapped in Pytest context managers like
``pytest.raises()`` as Act blocks.

It also recognises unittest's ``assertRaises()`` blocks as Act blocks.
