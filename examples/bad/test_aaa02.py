# NOTE: tests _can_ use pytest.raises() in Assert blocks. See discovery docs
# and examples/good/test_with_statement.py


def test() -> None:
    """
    Two result assignment statements will raise AAA02
    """
    x = 1
    y = 2

    result = x + y

    assert result == 3
    result = 2 * x + 2 * y
    assert result == 6


def test_act() -> None:
    """
    One result and act hint will raise
    """
    x = 1
    y = 2

    result = x + y

    assert result == 3  # act
