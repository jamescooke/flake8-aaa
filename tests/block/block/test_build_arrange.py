import ast

import pytest

from flake8_aaa.block import Block
from flake8_aaa.exceptions import EmptyBlock
from flake8_aaa.types import LineType


@pytest.mark.parametrize(
    'code_str', ['''
def test():
    x = 1
    y = 1

    result = x + y  # line 6

    assert result == 2
''']
)
def test_simple(first_node_with_tokens: ast.FunctionDef) -> None:
    result = Block.build_arrange(first_node_with_tokens.body, 6)

    assert result.first_line_no == 3
    assert result.last_line_no == 4
    assert result.line_type == LineType.arrange


@pytest.mark.parametrize(
    'code_str', [
        '''
def test(api_client, url):
    data = {  # line 3
        'user_id': 0,
        'project_permission': 'admin',
    }
    with catch_signal(user_perms_changed) as callback:  # line 7... keep going...

        result = api_client.put(url, data=data)

    assert result.status_code == 400
    assert callback.call_count == 0
    ''',
    ]
)
def test_context(first_node_with_tokens: ast.FunctionDef) -> None:
    """
    When context manager is in Arrange, the last line can include the Act line
    """
    result = Block.build_arrange(first_node_with_tokens.body, 9)

    assert result.first_line_no == 3
    assert result.last_line_no == 9
    assert result.line_type == LineType.arrange


# --- FAILURES ---


@pytest.mark.parametrize('code_str', ['''
def test():
    result = 1  # line 3

    assert result == 1
'''])
def test_none(first_node_with_tokens: ast.FunctionDef) -> None:
    """
    When no Arrange Block is found, EmptyBlock is raised
    """
    with pytest.raises(EmptyBlock):
        Block.build_arrange(first_node_with_tokens.body, 3)
