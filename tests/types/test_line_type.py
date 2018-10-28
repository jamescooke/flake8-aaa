import pytest

from flake8_aaa.types import LineType


@pytest.mark.parametrize('name, stringy', [
    ('func_def', 'def'),
    ('unprocessed', '???'),
])
def test_str(name, stringy):
    result = str(LineType[name])

    assert result == stringy
