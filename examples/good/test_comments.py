from typing import List, Union

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


# Example from docs:
# mark the end of the line considered the Act block with ``# act`` (case
# insensitive)
def test_Act() -> None:
    """
    Reverse shopping list operates in place

    AAA: act can be marked with "# Act"
    """
    shopping = ['apples', 'bananas', 'cabbages']

    shopping.reverse()  # Act

    assert shopping == ['cabbages', 'bananas', 'apples']


# Example from docs:
# can be marked with ``# act`` on the first or last line.


def test_mark_first_line() -> None:
    """
    Item can be added to list

    AAA: first line of act can be marked
    """
    shopping = ['apples', 'bananas', 'cabbages']

    shopping.append(  # act
        'dill',
    )

    assert shopping == ['apples', 'bananas', 'cabbages', 'dill']


def test_mark_last_line() -> None:
    """
    Item can be added to list

    AAA: last line of act can be marked
    """
    shopping: List[Union[str, List[str]]] = ['apples', 'bananas', 'cabbages']

    shopping.append([
        'dill',
        'eggs',
        'fennel',
    ])  # act

    assert shopping == [
        'apples',
        'bananas',
        'cabbages',
        ['dill', 'eggs', 'fennel'],
    ]


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


# Comments are OK in strings


def test_strings() -> None:
    special_chars = """
    #!$[]{}
    """.strip()

    result = len(special_chars)

    assert result == 7


def test_string_act():
    result = """
# Not a comment - it's a string
"""

    assert len(result) == 33


# Comment are OK before the test


# NOTE: igore this comment
def test_empty() -> None:
    result: List[int] = list()

    assert len(result) == 0
