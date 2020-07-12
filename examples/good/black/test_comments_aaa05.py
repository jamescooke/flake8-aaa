import pytest


def test_arrange():
    x = 3
    # Let's make a 3, 4, 5 triangle
    y = 4

    result = x ** 2 + y ** 2

    assert result == 25


def test_assert():
    result = list()

    assert not result
    # A copy of nothing is nothing
    assert result.copy() == []


def test_all():
    """
    Blank lines everywhere
    """
    x = 1
    # From zero
    y = 0

    with pytest.raises(ZeroDivisionError):
        # ... to infinity and beyond
        x / y

    assert x == 1
    # All still the same
    assert y == 0
