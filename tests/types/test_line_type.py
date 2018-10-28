import pytest

from flake8_aaa.types import LineType


@pytest.mark.parametrize(
    'name, stringy', [
        ('act_block', 'ACT'),
        ('arrange_block', 'ARR'),
        ('func_def', 'DEF'),
        ('unprocessed', '???'),
    ]
)
def test_str(name, stringy):
    result = str(LineType[name])

    assert result == stringy
