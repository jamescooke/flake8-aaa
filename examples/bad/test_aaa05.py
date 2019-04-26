import pytest


def test_arrange():
    """
    Blank line in Arrange Block
    """
    x = 3

    y = 4

    result = x ** 2 + y ** 2

    assert result == 25


def test_act():
    """
    Blank line in Act Block
    """
    nothing = None

    with pytest.raises(AttributeError):

        nothing.get_something()


def test_assert():
    """
    Blank line in Assert Block
    """
    result = list()

    assert not result

    assert result.copy() == []


def test_all(
    fixture_a,

    fixture_b,
):
    """
    Blank lines everywhere

    But the ones in the docstring don't count
    """
    x = 1

    y = 0

    with pytest.raises(ZeroDivisionError):

        x / y

    assert x == 1

    assert y == 0
