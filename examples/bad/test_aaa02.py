def test() -> None:
    x = 1
    y = 2

    result = x + y

    assert result == 3

    result += result

    assert result == 6
