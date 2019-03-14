import pytest

from flake8_aaa.types import LineType


@pytest.mark.parametrize(
    'name, stringy', [
        ('act', 'ACT'),
        ('arrange', 'ARR'),
        ('_assert', 'ASS'),
        ('func_def', 'DEF'),
        ('unprocessed', '???'),
    ]
)
def test_str(name, stringy):
    result = str(LineType[name])

    assert result == stringy
