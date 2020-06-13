# Example from AAA06 doc:


def test() -> None:
    shopping = ['apples', 'bananas', 'cabbages']

    # Reverse shopping list operates in place
    shopping.reverse()  # act

    assert shopping == ['cabbages', 'bananas', 'apples']


# --- OTHERS ---


def test_comment_after_act() -> None:
    x = 1
    y = 2

    result = x + y
    # Now check result

    assert result == 3
