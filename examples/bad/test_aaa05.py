import pytest


@pytest.fixture
def fixture_a() -> str:
    return 'A pointless fixture'


@pytest.fixture
def fixture_b() -> str:
    return 'Another pointless fixture'


# --- TESTS ---


def test_arrange() -> None:
    """
    Blank line in Arrange Block
    """
    x = 3

    y = 4

    result = x**2 + y**2

    assert result == 25


def test_act() -> None:
    """
    Blank line in Act Block
    """
    empty: list = []

    with pytest.raises(IndexError):

        empty[0]


def test_assert() -> None:
    """
    Blank line in Assert Block
    """
    result: list = list()

    assert not result

    assert result.copy() == []


def test_all(
    fixture_a: str,

    fixture_b: str,
) -> None:
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
