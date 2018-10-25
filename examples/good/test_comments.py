# Test for various comments before and after test blocks


def test_comment_before_act():
    x = 1
    y = 2

    # Sum x and y
    result = x + y

    assert result == 2


def test_comment_after_act():
    x = 1
    y = 2

    result = x + y
    # Sum x and y

    assert result == 2


def test_comment_before_assert():
    x = 1
    y = 2

    result = x + y

    # Always 2
    assert result == 2
