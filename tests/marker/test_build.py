import pytest

from flake8_aaa.exceptions import NotAMarker
from flake8_aaa.marker import Marker


@pytest.mark.parametrize('code_str', [
    '# AAA Act',
    '# AAA act',
    '# aaa act',
])
def test(code_str, first_token):
    result = Marker.build(first_token)

    assert isinstance(result, Marker)
    assert result.token.string == code_str


@pytest.mark.parametrize(
    'code_str', [
        '#  aaa act ',
        '#  aaa act',
        '# aaa act other stuff',
        '# aaa_act',
        '# stuff',
        '## noqa',
        'aaa = act + 1',
        'aaa  # noqa',
    ]
)
def test_not_a_marker(first_token):
    with pytest.raises(NotAMarker):  # noqa
        Marker.build(first_token)
