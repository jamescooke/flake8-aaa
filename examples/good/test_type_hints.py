def add_one(x: int) -> int:
    return x + 1


# Example from https://github.com/jamescooke/flake8-aaa/issues/122


def test_add_one() -> None:
    # Arrange.
    data: int = 0

    # Act.
    result: int = add_one(data)

    # Assert.
    assert result != data
    assert result == data + 1
