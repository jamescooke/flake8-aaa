import pytest


def test():
    result = 1

    assert result == 1


def test_x():
    x = 1
    y = 2

    result = x + y

    assert result == 3


def test_not_loaded(person):
    """
    Person can't be loaded
    """
    with pytest.raises(KeyError):
        person.load(-1)

    assert person.loaded is False
