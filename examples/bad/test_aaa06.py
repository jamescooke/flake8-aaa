import pytest

# Example from AAA06 doc:


def test_a() -> None:
    shopping = ['apples', 'bananas', 'cabbages']

    # Reverse shopping list operates in place
    shopping.reverse()  # act

    assert shopping == ['cabbages', 'bananas', 'apples']


def test_b() -> None:
    # NOTE: the most interesting thing about this test is this comment
    result = 1 + 1

    assert result == 2


# --- OTHERS ---


def test_act() -> None:
    nothing = None

    with pytest.raises(AttributeError):
        # You can't get something from nothing
        nothing.get_something()


def test_comment_after_act() -> None:
    x = 1
    y = 2

    result = x + y
    # Now check result

    assert result == 3


def test_raises() -> None:
    nothing = None

    with pytest.raises(AttributeError):
        # You can't get something from nothing
        nothing.get_something()
