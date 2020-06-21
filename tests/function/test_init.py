import pytest

from flake8_aaa.function import Function
from flake8_aaa.helpers import get_first_token, get_last_token
from flake8_aaa.types import LineType


@pytest.mark.parametrize('code_str', ['''

def test():
    pass

def test_other():
    pass

# All done :D
'''])
def test(first_node_with_tokens, lines, tokens):
    result = Function(first_node_with_tokens, lines, tokens)

    assert result.node == first_node_with_tokens
    assert result.lines == [
        'def test():\n',
        '    pass\n',
    ]
    assert result.act_node is None
    assert result.line_markers.types == [LineType.unprocessed, LineType.unprocessed]
    assert result.line_markers.fn_offset == 3
    assert result.first_line_no == 3
    assert result.tokens == tokens


@pytest.mark.parametrize(
    'code_str', [
        '''
# Test stuff

@pytest.mark.skip(reason='maths is too hard :D')
@pytest.mark.parametrize('value', [
    1,
    2,
    3,
])
def test(value):
    result = 1 + value

    assert result == 1
''',
    ]
)
def test_with_decorators(first_node_with_tokens, lines, tokens):
    result = Function(first_node_with_tokens, lines, tokens)

    assert result.first_line_no == 4
    assert get_first_token(result.node).line == "@pytest.mark.skip(reason='maths is too hard :D')\n"
    assert get_last_token(result.node).line == '    assert result == 1\n'
    assert len(result.lines) == 10
