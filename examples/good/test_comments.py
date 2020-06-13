# Example from AAA06 doc:
# * inline comment is OK for marking


def test() -> None:
    """
    Reverse shopping list operates in place
    """
    shopping = ['apples', 'bananas', 'cabbages']

    shopping.reverse()  # act

    assert shopping == ['cabbages', 'bananas', 'apples']


def test_ignore_typing() -> None:
    """
    Reverse shopping list operates in place
    """
    shopping = ['apples', 'bananas', 'cabbages']

    result = shopping.reverse()  # type: ignore

    assert result is None
    assert shopping == ['cabbages', 'bananas', 'apples']


# Comments are OK in Arrange and Assert.


def test_in_arrange():
    x = 3
    # Let's make a 3, 4, 5 triangle
    y = 4

    result = x**2 + y**2

    assert result == 25


def test_end_arrange() -> None:
    x = 1
    y = 2
    # Now test...

    result = x + y

    assert result == 3


def test_in_assert():
    result = list()

    assert not result
    # A copy of nothing is nothing
    assert result.copy() == []


def test_startassert() -> None:
    x = 1
    y = 2

    result = x + y

    # Always 3
    assert result == 3
