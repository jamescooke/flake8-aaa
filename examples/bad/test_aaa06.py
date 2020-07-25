import pytest

# Example from AAA06 doc:


def test() -> None:
    shopping = ['apples', 'bananas', 'cabbages']

    # Reverse shopping list operates in place
    shopping.reverse()  # act

    assert shopping == ['cabbages', 'bananas', 'apples']


def test_act():
    nothing = None

    with pytest.raises(AttributeError):
        # You can't get something from nothing
        nothing.get_something()


# --- OTHERS ---


def test_comment_after_act() -> None:
    x = 1
    y = 2

    result = x + y
    # Now check result

    assert result == 3


def test_raises():
    nothing = None

    with pytest.raises(AttributeError):
        # You can't get something from nothing
        nothing.get_something()
