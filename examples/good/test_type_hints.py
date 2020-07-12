def add_one(x: int) -> int:
    return x + 1


# Example from https://github.com/jamescooke/flake8-aaa/issues/122


def test_add_one() -> None:
    """
    Addition of type hint in act block does not prevent act block being found

    Note:
        Comment above Act line removed as of AAA06.
    """
    # Arrange.
    data: int = 0

    result: int = add_one(data)

    # Assert.
    assert result != data
    assert result == data + 1
