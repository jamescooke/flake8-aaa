import pytest

from flake8_aaa.marker import Marker


@pytest.mark.parametrize('code_str', ['# stuff'])
def test(first_token):
    result = Marker(first_token)

    assert result.token == first_token
