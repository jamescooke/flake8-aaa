import pytest
from faker import Faker

from flake8_aaa.block import Block
from flake8_aaa.types import LineType


def test(faker: Faker) -> None:
    result = Block(17, 19, LineType.act)

    assert isinstance(result, Block)
    assert result.first_line_offset == 17
    assert result.last_line_offset == 19
    assert result.line_type == LineType.act


# --- FAILURES ---


def test_before_start(faker: Faker) -> None:
    """
    First line number is before start of test function
    """
    first_line_offset = faker.pyint(max_value=0)
    last_line_offset = faker.pyint(min_value=1)
    line_type = faker.enum(LineType)

    with pytest.raises(AssertionError):
        Block(first_line_offset, last_line_offset, line_type)


def test_empty(faker: Faker) -> None:
    """
    First line number is greater than last line number
    """
    first_line_offset = faker.pyint(min_value=1)
    last_line_offset = first_line_offset - 1
    line_type = faker.enum(LineType)

    with pytest.raises(AssertionError):
        Block(first_line_offset, last_line_offset, line_type)
